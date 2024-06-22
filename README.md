# Test "client" for using Supatool

This is an example langchain project that uses the Supatoolkit to choose and execute tools.


need



could continue with current structure and use connery to generalize input to execute tool
- the dummy tool service gives back execute metadata and input args independently
- then hopefully the llm fills like the args correctly?
- is there some way to predfine the expected args?
  - maybe no way to validate but it feels the same/idk i think connery solves this

could work with the OpenAPI planner example
- work to extract and abstract the planning logic
- or just keep it all in one for now
- the main thing is how to get a new openapi on the fly with this system


or could start on the registry
-


gotta avoid getting sucked into the planning business
we just need something quick and dirty to test with
