def configure_script(script_file_contents):
    # Adding shebang to file
    parsed_response = "#!/usr/bin/env bash\n" + script_file_contents

    # Import environment variables from AWS and add to bash file
    for var_name, var_value in os.environ.items():
        # Exclude AWS-specific environment variables
        if var_name.startswith('AWS_'):
            continue
        parsed_response += f"export {var_name}='{var_value}'\n"

    return parsed_response