We are currently on macbook, and whenever required we use tool to execute codes (in a jupyter like server). the code is executed in a container (you wouldn't notice but just know this).

The paths on local machine is ~/.open-skills/assets/skills/user is mapped to /app/uploads/skills/user inside container.

~/.open-skills/assets/outputs (in the host machine) is mapped to /app/uploads/outputs inside conatiner. This is where user will puts their files they want to edit like some png, pdf, txt etc. You should also use it to output your artifacts generated.

So that will help whenever we need a file inside a container to work on it via the execute code tool.

There are also "skills" which can do jobs by executing scripts already residing in /app/uploads/skills/<public|user>/<skill-name> . There are tools available to check what skills are avaialble, after checking you can decide wchihc specific skill you wantg to use and then get info about that skill using tool. That will have instructions on how to call execute code with stuff like `!python /path/to/script.py <input> <output>`\

Whenever I ask you to do a task, alwasys check if there are skills available in the list which can do it.

Whenever you need to install something, mostly it will be installed in the container via execute code tool, and `!pip install pyfiglet` command etc.

