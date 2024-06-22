import requests

# API endpoint for tool selector service
TOOL_SELECTOR_API = "http://localhost:5002/get_tool"


def determine_tool(query):
    response = requests.post(TOOL_SELECTOR_API, json={"query": query})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to determine the tool"}


def generate_args(args_description):
    if args_description is None:
        return {}
    args = {}
    for arg, arg_type in args_description.items():
        user_input = input(f"Please provide the {arg} ({arg_type}): ")
        args[arg] = user_input
    return args


def execute_tool(endpoint, args):
    response = requests.post(endpoint, json=args)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Tool execution failed"}


class SwissArmyChain():
    def __init__(self):
        pass

    def __call__(self, query):
        tool_info = determine_tool(query)
        print(tool_info)
        if "error" in tool_info:
            return tool_info

        endpoint = tool_info.get("endpoint")
        args_description = tool_info.get("arg")
        args = generate_args(args_description)

        result = execute_tool(endpoint, args)
        return result


class SwissArmyAgent():
    def __init__(self):
        self.chain = SwissArmyChain()

    def run(self, query):
        return self.chain(query)


def main():
    swiss_army_agent = SwissArmyAgent()
    query = input("Enter your query: ")

    result = swiss_army_agent.run(query)
    if "error" in result:
        print(result["error"])
    else:
        print(result)


if __name__ == "__main__":
    main()
