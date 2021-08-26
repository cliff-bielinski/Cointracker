import configparser

def config(section, file='database.ini'):
    """parses through a file and returns configuration settings for a given section in an INI file
    
    Args:
        section (str) - name of the section in the configuration INI file
        file (str) - file name of INI file
    
    Returns:
        configuration (obj) - a configuration object with config settings from INI file
    """

    configuration = configparser.ConfigParser()
    configuration.read(file)
    db_config = {}

    if configuration.has_section(section):
        params = configuration.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    
    else:
        raise Exception('{0} not found in the {1} file'.format(section, file))
    
    return db_config