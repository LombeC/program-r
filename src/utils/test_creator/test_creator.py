import xml.etree.ElementTree as ET
import sys
from programr.parser.template.nodes.bot import TemplateBotNode
from programr.parser.template.nodes.get import TemplateGetNode
from programr.clients.client import BotClient
from programr.clients.events.console.config import ConsoleConfiguration

class TestCreatorBotClient(BotClient):

    def __init__(self):
        BotClient.__init__(self, "TestCreator")

    @property
    def test_dir(self):
        return self.arguments.args.test_dir

    @property
    def test_file(self):
        return self.arguments.args.test_file

    @property
    def qna_file(self):
        return self.arguments.args.qna_file

    @property
    def verbose(self):
        return self.arguments.args.verbose

    def get_description(self):
        return 'ProgramR Test Creator Client'

    def add_client_arguments(self, parser=None):
        if parser is not None:
            parser.add_argument('--aiml_file', dest='aiml_file', help='AIML File to create tests from')
            parser.add_argument('--test_file', dest='test_file', help='Test file to create with associated unit tests')
            parser.add_argument('--ljust', dest='ljust', action='store_true', help='Left justifies the first csv column, a good value is 40 or 80')
            parser.add_argument('--replace_file', dest='replace_file', help='When creating tests you can specify replacements certain data types')

    def get_client_configuration(self):
        return ConsoleConfiguration()
            

def load_replacements(replace_file):
    texts = {}
    bots = {}
    sets = {}
    with open(replace_file, "r") as file:
        for line in file:
            line = line.strip()
            name_value = line.split(":")
            type_name = name_value[0].split(",")
            if len(type_name) == 2:
                if type_name[0] == "SET":
                    sets[type_name[1]] = name_value[1].upper()
                elif type_name[0] == "BOT":
                    bots[type_name[1]] = name_value[1].upper()
                else:
                    print("Unknown mapping type", type_name[0].upper())
            else:
                texts[type_name[0]] = name_value[1]

    return texts, sets, bots

def replace_wildcard(text, texts, wildcard):
    if wildcard in text and wildcard in texts:
        return text.replace(wildcard, texts[wildcard])
    return text

def replace_wildcards(text, texts):
    text = replace_wildcard(text, texts, "*")
    text = replace_wildcard(text, texts, "#")
    text = replace_wildcard(text, texts, "^")
    text = replace_wildcard(text, texts, "_")
    return text

def parse_categories(categories, output_file, bot_node, get_node):
    questions = []
    for category in categories:
        pattern_text = ""

        pattern = category.find("pattern")
        for elt in pattern.iter():

            if elt.tag == "pattern":
                text = elt.text.strip().upper()
                pattern_text += replace_wildcards(text, texts)

            elif elt.tag == "set":
                if 'name' in elt.attrib:
                    name = elt.attrib['name']
                else:
                    name = elt.text.strip()

                if name in sets:
                    pattern_text += sets[name]
                else:
                    pattern_text += "SET[%s]"%name

            elif elt.tag == "bot":
                if 'name' in elt.attrib:
                    name = elt.attrib['name']
                else:
                    name = elt.text.strip()

                if name in bots:
                    pattern_text += bots[name]
                else:
                    pattern_text += "BOT[%s]" % name
            
            # NOTE: Is this condition needed?
            elif elt.tag == "topic":
                topic_cats = elt.tag.findall("category")
                topic_questions = parse_categories(topic_cats, output_file, bot_node, get_node)

            pattern_text += " "

            if elt.tail is not None and elt.tail.strip() != "":
                text = elt.tail.strip().upper()
                pattern_text += replace_wildcards(text, texts)
                pattern_text += " "

        
        question = '"%s",'%pattern_text.strip()
        question = question.ljust(ljust)
        
        
        template = category.find('template')
        # print("Template: {}".format(template.text))
        # TODO: Need to parse bot, set, get tags
        string = "["
        tail = ""
        for elt in template.iter(): 
            tag = elt.tag
            
            if tag == "bot":
                string = bot_node.get_bot_variable(client_context, elt.attrib['name'])
                # print("Text after bot: {}".format(elt.tail))
                tail += elt.tail

            elif tag == "get":
                string = get_node.get_property_value(client_context, False, elt.attrib['name'])
                # print("Text after bot: {}".format(elt.tail))
                tail += elt.tail    
            
            elif tag == "random":
                lis = elt.findall("li")
                for li in lis:
                    print("li: {}".format(type(li)))
                    li_string = ""
                    for elem in li.iter():
                        bot_tail = ""
                        get_tail = ""
                        if elem.tag == "bot":
                            li_string += bot_node.get_bot_variable(client_context, elem.attrib['name'])
                            bot_tail = elt.tail  

                        elif elem.tag == "get":
                            li_string += get_node.get_property_value(client_context, False, elem.attrib['name'])
                            get_tail = elem.tail

                    if li.text is not None:
                        string += li.text
                        if bot_tail is not None and get_tail is not None:
                            string += li_string + bot_tail + get_tail + "; "
                        
                        elif bot_tail is not None and get_tail is None:
                            string += li_string + bot_tail + "; "

                        elif bot_tail is None and get_tail is not None:
                            string += li_string + get_tail + "; "
                        
                        else:
                            string += li.text + "; "
                            
                        string = string[:-2]
                        string += "]"

        # if len(li) > 0:
        #     test_line = '%s "%s"'%(question, string)
        # else:
        #     test_line = '%s "%s"'%(question, template.text)
        if template.text is None:
            response = string
            test_line = '%s "%s"'%(question, response)
        else:
            if tail is not None:
                response = template.text.strip() + string + tail
            else:
                response = template.text.strip() + string
            test_line = '%s "%s"'%(question, response)
        
        output_file.write(test_line)
        output_file.write("\n")
        
    print("completed")
    return questions

if __name__ == '__main__':

    aiml_file = sys.argv[4]
    test_file = sys.argv[6]
    # ljust = int(sys.argv[3])
    ljust = 20
    replace_file = sys.argv[8]

    print("aiml_file: {}".format(aiml_file))
    print("test_file: {}".format(test_file))
    print("ljust: {}".format(ljust))
    print("replace_file: {}".format(replace_file))

    client = TestCreatorBotClient()
    client_context = client.create_client_context(1, load_variables=False)
    bot_node = TemplateBotNode()
    get_node = TemplateGetNode()

    default = None
    # if len(sys.argv) > 5:
    #     default = sys.argv[5]

    print("loading in file: " + aiml_file + "...")
    # print("test_file:", test_file)
    # print("replace_file:", replace_file)
    # print("Default:", default)

    texts, sets, bots = load_replacements(replace_file)

    with open(test_file, "w+") as output_file:
        # if default is not None:
        #     output_file.write('$DEFAULT, "%s"\n\n'%default)
        try:
            tree = ET.parse(aiml_file)
            aiml = tree.getroot()
            categories = aiml.findall('category')

            questions = parse_categories(categories, output_file, bot_node, get_node)

        except Exception as e:
            print(e)
            line = "failed to load file: " + aiml_file + "\n"
            f = open("results/failed_loads.txt", "a")
            f.write(line)
            f.close()
        
        exit(0)