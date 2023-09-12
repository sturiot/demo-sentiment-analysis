import os
import logging.config
from typing import Any, Dict, Union
from pathlib import Path
from pyspark import SparkConf
from pyspark.sql import SparkSession
from kedro.framework.context import KedroContext
from kedro.config import TemplatedConfigLoader

logger = logging.getLogger(__name__)


class ProjecContext(KedroContext):

    def __init__(
        self,
        package_name: str,
        project_path: Union[Path, str],
        config_loader=None,
        env: str = None,
        extra_params: Dict[str, Any] = None,
        hook_manager=None
    ):

        super().__init__(
            package_name,
            project_path,
            config_loader,
            hook_manager,
            env,
            extra_params
        )

        self._init_env_vars()

        template_config_loader = TemplatedConfigLoader(
            conf_source=config_loader.conf_source,
            env=config_loader.env,
            globals_dict=os.environ
        )

        self._config_loader = template_config_loader

        self._create_spark_session()

    def _init_env_vars(self):
        env_params = self.config_loader.get("env*")
        self._set_os_environ(env_params)

    def _create_spark_session(self):
        
        if self.env == 'seldon': return
        
        logger.info("Initialize SparkSession")
        
        self.pyspark_submit_args_dic = {
            'lab_local': self._pyspark_submit_args_lab_local
        }
        
        self.pyspark_submit_args_dic[self.env]()

        spark_params = self.config_loader.get("spark*")
        spark_conf = SparkConf().setAll(spark_params.items())
        self.spark = (
            SparkSession.builder.config(conf=spark_conf)
            .enableHiveSupport()
            .getOrCreate()
        )

        self.spark.sparkContext.setLogLevel("INFO")

    def _pyspark_submit_args_lab_local(self):
        conda_path = self._get_lab_conda_path()
        conda_env = self._get_lab_conda_env()
        os.environ['PYSPARK_DRIVER_PYTHON'] = f"{conda_path}{conda_env}/bin/python"
        os.environ['PYSPARK_PYTHON'] = f"{conda_path}{conda_env}/bin/python"
        os.environ['PYSPARK_SUBMIT_ARGS'] = (
            " pyspark-shell"
        )
    
    def _set_os_environ(self, params: Dict):
        for k, v in params.items():
            os.environ[k] = v

    def _get_lab_conda_path(self) -> str:
        return os.environ["conda_env_path"]

    def _get_lab_conda_env(self) -> str:
        return os.environ["conda_env"]















