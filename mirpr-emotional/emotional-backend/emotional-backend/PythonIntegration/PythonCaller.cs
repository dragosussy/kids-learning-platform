using System.Collections.Generic;
using emotional_backend.Utilities;
using Newtonsoft.Json;

namespace emotional_backend.PythonIntegration
{
    public class PythonCaller
    {
        private readonly string _scriptPath; // path to the folder with the model
        private readonly string _callerPath; // path to the folder with the caller

        public PythonCaller(string scriptPath)
        {
            _callerPath =
                "E:\\Informatique\\University\\Anul3\\MIRPR\\mirpr-emotional\\emotional-backend\\emotional-backend\\PythonIntegration\\caller.py";
            _scriptPath = scriptPath;
        }
        
        public Dictionary<string, string> CallClassMethod(string className, string method, PythonCallerArgs args)
        {
            string argString = args.Serialized();

            var command = $"\"{_callerPath}\" \"{_scriptPath}\" \"{className}\" \"{method}\" \"{argString}\"";
            var processStatus = ProcessExecutor.Exec(command);

            var serializedResult = JsonConvert.DeserializeObject<Dictionary<string, string>>(processStatus.Result.Trim());
            return serializedResult;
        }
    }
}