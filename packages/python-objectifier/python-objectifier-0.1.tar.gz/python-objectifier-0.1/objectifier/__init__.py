class convert_json_to_object:
    def __init__(self, item):
        if isinstance(item, dict):
            class convert_dictionary_to_object(dict): # https://goodcode.io/articles/python-dict-object/
                def __getattr__(self, name):
                    if name in self:
                        return self[name]
                    else:
                        raise AttributeError("No such attribute: " + name)

                def __setattr__(self, name, value):
                    self[name] = value

                def __delattr__(self, name):
                    if name in self:
                        del self[name]
                    else:
                        raise AttributeError("No such attribute: " + name)

            return convert_dictionary_to_object(item)

        elif isinstance(item, list):
            updated_list = []
            for sub_item in item:
                updated_item = convert_json_to_object(sub_item)
                updated_list.append(updated_item)
                
            return updated_list