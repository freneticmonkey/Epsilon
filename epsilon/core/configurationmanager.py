import ConfigParser
import os

from epsilon.core.basesingleton import BaseSingleton
from epsilon.core.settings import Settings

class ConfigurationManager(BaseSingleton):

    @classmethod
    def load_configuration(cls):
        cls.get_instance()._load_configuration()

    @classmethod
    def save_configuration(cls):
        cls.get_instance()._save_configuration()

    def __init__(self):
        self._filename = 'settings.cfg'
        self._filepath = os.path.join(os.getcwd(), self._filename)

        self._config_exists = os.path.exists(self._filepath)

        self._config = ConfigParser.ConfigParser()

    def __del__(self):
        self.save_configuration()

    def _check_type(self, value):

        # Default to string
        value_type = "str"

        # Check Boolean
        if value == "True" or value == "False":
            value_type = "bool"
        
        # Check list
        elif value[0] == "[" and value[-1] == "]":
            value_type = "list"

        # Check int
        elif value.find('.') == -1:
            try:
                int(value)
                value_type = "int"
            except ValueError:
                pass

        elif value.find('.') > -1:
            try:
                float(value)
                value_type = "float"
            except ValueError:
                pass

        return value_type

    def _load_configuration(self):
        if self._config_exists:
            # If read ok
            read_result = self._config.read(self._filepath)

            if len(read_result) > 0 and os.path.basename(read_result[0]) == self._filename:

                # Populate the classes with the appropriate values
                for section in self._config.sections():
                    #print "Reading Config Section: " + section
                    
                    for option in self._config.options(section):
                        
                        value_type = "str"

                        # If the section has been defined in the default settings
                        if Settings.has_section(section):
                            value_type = Settings.get(section, option).__class__.__name__
                        
                        # Else use a manual technique to figure this out.
                        else:
                            value = self._config.get(section, option)
                            value_type = self._check_type( value )
                            
                        if value_type == "str":
                            Settings.set(section, option, self._config.get(section, option) )

                        elif value_type == "int":
                            Settings.set(section, option, self._config.getint(section, option) )

                        elif value_type == "float":
                            Settings.set(section, option, self._config.getfloat(section, option) )

                        elif value_type == "bool":
                            Settings.set(section, option, self._config.getboolean(section, option) )

                        elif value_type == "list":
                            # If the item is a list get it as a string and process it as appropriate
                            # only lists containing homogeneous values are supported

                            list_value = self._config.get(section, option)

                            # If the section has already been defined in the default settings
                            if Settings.has_section(section):
                                #assuming that the list has more than one value...
                                list_type = Settings.get(section, option)[0].__class__.__name__

                            # Otherwise extract the type
                            else:
                                #Extract the first list element

                                # Default to a single element list
                                list_element = list_value[1:-1]

                                #Check for more and adjust as necessary
                                if list_value.find(',') > 0:
                                    list_element = list_value[1:list_value.find(',')]

                                # Get the element_type
                                list_type = self._check_type( list_element )

                            # In place of python's lack of a switch statement, defaulting to str if None
                            cast_func = { 'int' : int, 'float' : float, 'bool' : bool, 'str' : str, 'NoneType' : str }[list_type]

                            # Generate a list from the string
                            Settings.set(section, option, [cast_func(value) for value in list_value[1:-1].split(',')] )



                        value = self._config.get(section, option)
                        # print "Reading property class: %s name: %s value: %s" % ( section, option, str(value) )
                        # print "Class value class: %s name: %s value: %s valuetype: %s" % ( section, option, str(Settings.get(section, option)), Settings.get(section, option).__class__ )
        else:
            print "Can't find configuration file: %s " % self._filename

    def _save_configuration(self):
        print "Shutting down ConfigurationManager"
        # For each of the settings sections
        for section in Settings.get_sections():
            # if they don't yet have a section in the settings file, add one.
            if not section in self._config.sections():
                self._config.add_section(section)

            # Store their values
            for option in Settings.get_options(section):
                value = Settings.get(section, option)
                self._config.set(section, option, value )

                # print "Class value class: %s name: %s value: %s valuetype: %s" % ( section, option, value, value.__class__)

        # for class_def in self._settings_classes:
        #     class_name = class_def.__name__

        #     # if they don't yet have a section in the settings file, add one.
        #     if not class_name in self._config.sections():
        #         self._config.add_section(class_name)

        #     # Store their values
        #     for name, value in class_def.__dict__.iteritems():
        #         # Ignoring generated class properties
        #         if name[:2] != "__":
        #             self._config.set(class_name, name, value)
        #             print "Class value class: %s name: %s value: %s valuetype: %s" % ( class_name, name, value, value.__class__)

        with open(self._filepath, 'w') as configfile:
            self._config.write(configfile)