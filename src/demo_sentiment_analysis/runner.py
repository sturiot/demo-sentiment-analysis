from kedro.framework.project import configure_project
from kedro.framework.session import KedroSession

def run_pipeline(pipeline_name="__default__", env="base", extra_params={}):
    package_name = "demo_seniment_analysis"
    configure_project(package_name)
    with KedroSession.create(package_name=package_name, env=env, extra_params=extra_params) as session:
        session.run(piplein_name=piplein_name)
