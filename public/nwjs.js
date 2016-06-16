function quit()
{
    var gui = require("nw.gui");
    gui.App.quit();
}

function argv(idx)
{
    var gui = require("nw.gui");

    if( typeof idx != "undefined" )
    {
        if( idx >= 0 && idx < gui.App.argv.length )
            return gui.App.argv[idx];

        return null;
    }

    return gui.App.argv;
}

function readFile(filename, notifier)
{
    var fs = require("fs");

    fs.readFile(filename, "utf-8",
        function(err, data)
        {
            if( err )
            {
                alert(err);
                quit();
            }

            var elem;

            if( ( elem = document.getElementById(notifier) ) )
            {
                elem.setAttribute("data-content", data);
                elem.click(); /* Invoke! */
            }
            else
            {
                alert("Error: An element with the ID '" + notifier + "' could not be found.");
                quit();
            }
        });
}

function shell(command, notifier)
{
    var exec = require("child_process").exec;

    notifier.innerHTML = "";

    exec(command, function(error, stdout, stderr)
        {
            if( error )
            {
                notifier.innerHTML(`exec error: ${error}`);
                return;
            }

            notifier.innerHTML += stdout + stderr;
        });
}

global.shell = shell;
global.readFile = readFile;
global.quit = quit;
global.argv = argv;
