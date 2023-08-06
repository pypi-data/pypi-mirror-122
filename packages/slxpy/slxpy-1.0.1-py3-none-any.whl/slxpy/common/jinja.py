import jinja2

def create_jinja_env(package_path: str):
    loader = jinja2.PackageLoader(
        package_name="slxpy.templates",
        package_path=package_path,
        encoding="utf-8"
    )
    env = jinja2.Environment(
        # extensions=['jinja2.ext.debug'],
        loader=loader,
        auto_reload=False,
        autoescape=False,
        keep_trailing_newline=True,
        # trim_blocks=True,
    )
    env.policies['json.dumps_kwargs'] = {'sort_keys': True, 'ensure_ascii': False}
    return env
