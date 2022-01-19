using System.Diagnostics;
using System.IO;

namespace emotional_backend.Utilities
{
    public static class ProcessExecutor
    {
        public static (string Result, string Error) Exec(string args)
        {
            var process = new ProcessStartInfo()
            {
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true,
                WindowStyle = ProcessWindowStyle.Hidden,
                FileName = "C:\\Users\\drago\\AppData\\Local\\Programs\\Python\\Python39\\python.exe",
                Arguments = args
            };

            var results = "";
            var errors = "";
            using (var startedProcess = Process.Start(process))
            {
                using (StreamReader reader = startedProcess.StandardOutput)
                {
                    results = reader.ReadToEnd();
                }
                using (StreamReader reader = startedProcess.StandardError)
                {
                    errors = reader.ReadToEnd();
                }
                
                startedProcess.WaitForExit();
            }

            return (results, errors);
        }
    }
}