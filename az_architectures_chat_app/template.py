from jinja2 import Environment, FileSystemLoader


class JinjaPromptTemplate:
    def execute(self, template_path, **kwargs) -> str:
        print(f"template_path: {template_path} kwargs: {kwargs}")
        # Extract the directory path and template file name
        template_dir, template_file = template_path.rsplit("/", 1)

        # Create a Jinja2 environment with the provided template directory
        loader = FileSystemLoader(template_dir)
        env = Environment(loader=loader)

        # Load the template from the file
        template = env.get_template(template_file)

        # Render the template with the provided kwargs
        result = template.render(**kwargs)

        return result
