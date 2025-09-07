from functools import lru_cache
from os import path
from pydantic_settings import BaseSettings
from pydantic import Field

__all__ = ['get_settings']

ENV_FILES = ('.env', '.env.prod')
ROOT_PATH = path.dirname(path.abspath(path.join(__file__, '..')))


class Settings(BaseSettings):
    """应用配置
        server目录为后端项目根目录, 在该目录下创建 ".env" 文件, 写入环境变量(默认大写)会自动加载, 并覆盖同名配置(小写)
            eg.
            .env 文件内写入:
                UPLOAD_DIRECTORY='/tmp/test/'
                REDIS_URL='redis://localhost:6379'
                DATABASE_URL='mysql+pymysql://root:root@localhost:3306/likeadmin?charset=utf8mb4'

                上述环境变量会覆盖 upload_directory 和 redis_url
    """
    # 上传文件路径
    upload_directory: str = Field(default='/tmp/uploads/likeadmin-python/', env='UPLOAD_DIRECTORY')
    # 上传图片限制
    upload_image_size: int = 1024 * 1024 * 10  # 明确标注为 int 类型
    # 上传视频限制
    upload_video_size: int = 1024 * 1024 * 30  # 明确标注为 int 类型
    # 上传图片扩展
    upload_image_ext: set[str] = {'png', 'jpg', 'jpeg', 'gif', 'ico', 'bmp'}  # 明确标注为 set[str] 类型
    # 上传视频扩展
    upload_video_ext: set[str] = {'mp4', 'mp3', 'avi', 'flv', 'rmvb', 'mov'}  # 明确标注为 set[str] 类型
    # 上传路径URL前缀
    upload_prefix: str = '/api/uploads'  # 明确标注为 str 类型

    # 数据源配置
    database_url: str = Field(
        default='mysql+pymysql://root:root@localhost:3306/likeadmin?charset=utf8mb4',
        env='DATABASE_URL'
    )
    # 数据库连接池最小值
    database_pool_min_size: int = 5
    # 数据库连接池最大值
    database_pool_max_size: int = 20
    # 数据库连接最大空闲时间
    database_pool_recycle: int = 300

    # Redis源配置
    redis_url: str = Field(default='redis://localhost:6379', env='REDIS_URL')

    # 是否启用静态资源
    enabled_static: bool = True
    # 静态资源URL路径
    static_path: str = '/api/static'  # 明确标注为 str 类型
    # 静态资源本地路径
    static_directory: str = path.join(ROOT_PATH, 'static')

    # CORS 跨域资源共享
    # 允许跨域的源列表 eg. '["*"]'   '["http://localhost", "http://localhost:8080", "https://www.example.org"]'
    cors_allow_origins: str = '["*"]'  # 明确标注为 str 类型

    # 模式
    mode: str = Field(default='prod', env='MODE')  # dev, prod

    # 全局配置
    # 版本
    version: str = 'v1.1.0'
    # 项目根路径
    root_path: str = ROOT_PATH
    # 默认请求超时
    request_timeout: int = 15
    # Mysql表前缀
    table_prefix: str = 'la_'
    # 时区
    timezone: str = 'Asia/Shanghai'
    # 日期时间格式
    datetime_fmt: str = '%Y-%m-%d %H:%M:%S'
    # 系统加密字符
    secret: str = Field(default='UVTIyzCy', env='SECRET')
    # Redis键前缀
    redis_prefix: str = 'Like:'
    # 短信验证码
    redis_sms_code: str = 'smsCode:'
    # 禁止修改操作 (演示功能,限制POST请求)
    disallow_modify: bool = False
    # 当前域名
    domain: str = Field(default='http://127.0.0.1:8000', env='DOMAIN')  # 明确标注为 str 类型
    # 短信验证码
    redisSmsCode: str = "smsCode:"  # 明确标注为 str 类型

    # 配置模型设置
    model_config = {
        "env_file": [path.join(ROOT_PATH, f) for f in ENV_FILES],
        "env_file_encoding": 'utf-8',
        "extra": "allow"
    }


@lru_cache()
def get_settings() -> Settings:
    """获取并缓存应用配置"""
    return Settings()
    