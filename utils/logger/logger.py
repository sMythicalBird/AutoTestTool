# -*- coding: utf-8 -*-
"""
@file:      logger.py
@time:      2025/9/26 04:03
@author:    sMythicalBird
"""
"""
现代化的日志模块，基于TOML配置，支持轮转、模块过滤、异常捕获。
"""
import logging
import logging.handlers
from pathlib import Path
from typing import Any, Dict, Optional
from zoneinfo import ZoneInfo
import tomllib  # Python 3.11+ 内置
import sys

# =============================
# 自定义时区格式化器
# =============================
class TimezoneFormatter(logging.Formatter):
    def __init__(self, fmt: str, datefmt: Optional[str], timezone: str = "UTC"):
        super().__init__(fmt, datefmt=datefmt, style="{")
        self.tz = ZoneInfo(timezone)

    def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None) -> str:
        import datetime

        dt = datetime.datetime.fromtimestamp(record.created, tz=self.tz)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()


# =============================
# 日志管理器主类
# =============================
class StructuredLogger:
    """
    基于 TOML 配置的日志系统，支持轮转、JSON、时区等。
    """

    def __init__(self, config_path: Path) -> None:
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self._load_config()
        self._setup_logging()

    def _load_config(self) -> None:
        """加载 TOML 配置文件"""
        try:
            with open(self.config_path, "rb") as f:
                full_config = tomllib.load(f)
            self.config = full_config["log"]
        except Exception as e:
            raise RuntimeError(f"❌ 无法加载日志配置 {self.config_path}: {e}")

    def _setup_logging(self) -> None:
        """配置日志系统"""
        log_level = getattr(logging, self.config["level"].upper(), logging.INFO)
        log_dir = Path(self.config["log_dir"])
        log_dir.mkdir(exist_ok=True, parents=True)

        # 获取根日志器
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        root_logger.handlers.clear()  # 清除默认 handler

        # =============================
        # 1. 控制台处理器
        # =============================
        if "handlers" in self.config and "console" in self.config["handlers"]:
            console_level = self.config["handlers"]["console"].get("level", "INFO").upper()
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(console_level)
            formatter = self._create_formatter("console")
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)

        # =============================
        # 2. 文件处理器（按天轮转）
        # =============================
        log_file = log_dir / "app.log"
        when = self.config["handlers"]["file"].get("when", "midnight")
        interval = self.config["handlers"]["file"].get("interval", 1)
        backup_count = self.config["backup_count"]
        encoding = self.config["handlers"]["file"].get("encoding", "utf-8")

        file_handler = logging.handlers.TimedRotatingFileHandler(
            log_file,
            when=when,
            interval=interval,
            backupCount=backup_count,
            encoding=encoding,
            utc=False,
        )
        file_formatter = self._create_formatter("file")
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

    def _create_formatter(self, handler_type: str) -> logging.Formatter:
        """根据处理器类型创建格式器"""
        use_json = self.config.get("use_json", False)
        timezone = self.config.get("timezone", "UTC")

        # =============================
        # 1. 文件处理器：支持 JSON
        # =============================
        if handler_type == "file":
            if use_json:
                try:
                    from pythonjsonlogger.jsonlogger import JsonFormatter
                    fmt = self.config["formatters"]["json"].get("format", "%(message)s")
                    return JsonFormatter(fmt)
                except ImportError:
                    logging.warning("⚠️ python-json-logger 未安装，回退到默认格式")
                    use_json = False

            # 文件用默认格式（无颜色）
            fmt_config = self.config["formatters"]["default"]
            fmt = fmt_config["format"]
            datefmt = fmt_config.get("datefmt")
            return TimezoneFormatter(fmt=fmt, datefmt=datefmt, timezone=timezone)

        # =============================
        # 2. 控制台处理器：优先尝试彩色
        # =============================
        if handler_type == "console":
            # 检查是否配置了 'colored' 格式
            if "formatters" in self.config and "colored" in self.config["formatters"]:
                try:
                    import colorlog
                    from colorlog import ColoredFormatter

                    # 获取彩色格式配置
                    colored_config = self.config["formatters"]["colored"]
                    fmt = colored_config["format"]
                    datefmt = colored_config.get("datefmt")
                    style = colored_config.get("style", "{")
                    log_colors = colored_config.get("colors", {
                        'DEBUG': 'cyan',
                        'INFO': 'green',
                        'WARNING': 'yellow',
                        'ERROR': 'red',
                        'CRITICAL': 'bold_red',
                    })

                    # 返回 ColoredFormatter（注意：它不支持直接传 timezone）
                    return ColoredFormatter(
                        fmt,
                        datefmt=datefmt,
                        style=style,
                        log_colors=log_colors
                    )
                except ImportError:
                    logging.warning("⚠️ colorlog 未安装，控制台日志将无颜色")

            # 回退到默认格式（仍带时区）
            fmt_config = self.config["formatters"]["default"]
            fmt = fmt_config["format"]
            datefmt = fmt_config.get("datefmt")
            return TimezoneFormatter(fmt=fmt, datefmt=datefmt, timezone=timezone)

        # 默认格式
        fmt_config = self.config["formatters"]["default"]
        fmt = fmt_config["format"]
        datefmt = fmt_config.get("datefmt")
        return TimezoneFormatter(fmt=fmt, datefmt=datefmt, timezone=timezone)

    def get_logger(self, name: str) -> logging.Logger:
        """获取按模块命名的日志器"""
        return logging.getLogger(name)

    def log_exception(
        self,
        logger: logging.Logger,
        message: str,
        exc_info: bool = True,
        **kwargs: Any,
    ) -> None:
        """增强版异常日志，支持颜色输出（控制台）"""
        # ANSI 颜色：红色加粗
        colored_msg = f"\033[1;31m❌ {message}\033[0m"
        logger.error(colored_msg, exc_info=exc_info, extra=kwargs)


# =============================
# 全局实例：供外部直接使用
# =============================
_CONFIG_PATH = Path(__file__).parent / "logger_config.toml"
logger_manager = StructuredLogger(_CONFIG_PATH)
logger = logger_manager.get_logger("root")

# =============================
# 便捷函数（可选）
# =============================
def info(msg: str, **kwargs: Any) -> None:
    logger.info(msg, extra=kwargs)


def error(msg: str, **kwargs: Any) -> None:
    logger.error(msg, extra=kwargs)


def debug(msg: str, **kwargs: Any) -> None:
    logger.debug(msg, extra=kwargs)


def warning(msg: str, **kwargs: Any) -> None:
    logger.warning(msg, extra=kwargs)


def critical(msg: str, **kwargs: Any) -> None:
    logger.critical(msg, extra=kwargs)


# =============================
# 模块导出
# =============================
__all__ = [
    "logger",
    "logger_manager",
    "info",
    "error",
    "debug",
    "warning",
    "critical",
    "StructuredLogger",
]









