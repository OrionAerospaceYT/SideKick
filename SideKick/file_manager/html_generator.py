"""
Generates html for the boards and library managers.
(IDK WHY THIS IS IN FILE MANAGER TODO)
"""

class HtmlGenerator():
    """
    Holds the functions which generate html for JsonLibraryManager and
    JsonBoardsManager.
    """

    def get_versions(self, name, my_dict):
        """
        Returns all of the versions that are avaliable.
        """

        return list(my_dict[name]["version"])

    def get_title(self, name):
        """
        Returns the formatting for a title on the QTextBrowser of libraries
        that can be installed.

        Args:
            name (string): the text for the title (name)
        """

        return f"<h1><p style=\"color:#00f0c3\">{name}</p></h1><br>"

    def get_link(self, link):
        """
        Returns the html link for categories which are links.

        Args:
            name (string): the link
        """

        return f"<a style=\"color:#8ab4f8\" href={link}>{link}</a><br>"

    def get_paragraph(self, name, text):
        """
        Makes a paragraph for each sub category

        Args:
            name (string): the name of the category
            text (string): the description
        """
        return f"<p>{name}: {text}</p>"

    def get_list_paragraph(self, name, my_list):
        """
        Makes a paragraph for each sub category

        Args:
            name (string): the name of the category
            list (list): the description
        """
        string = f"<p>{name}:"
        for item in my_list:
            string += f"<br>{item}"
        return string

    def get_html(self, name, my_dict):
        """
        Formats the library text for the display on library manager options
        
        Args:
            name (str): the name of the dictionary item
            my_dict (dictionary): the dictionary to parse into html
        """
        html = self.get_title(name)

        for item in list(my_dict[name].keys()):
            info = my_dict[name][item]

            if item == "version":
                continue
            if item in ("repository", "url", "website"):
                html += self.get_link(str(info))
            elif isinstance(info, list):
                html += self.get_list_paragraph(item, info)
            elif isinstance(item, str):
                html += self.get_paragraph(item, str(info))

        return html
