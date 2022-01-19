using System.Collections.Generic;
using emotional_backend.PythonIntegration;

namespace emotional_backend.Utilities
{
    public static class AiTools
    {
        private static readonly string _pathToPythonModuleFolder =
            "E:\\Informatique\\University\\Anul3\\MIRPR\\mirpr-emotional";

        private static readonly PythonCaller _pythonCaller = new PythonCaller(_pathToPythonModuleFolder);
        
        public static IDictionary<string, string> RecognizeFace(string imagePath)
        {
            var arguments = new PythonCallerArgs()
                .AddArgument("imagePath", imagePath);
            return _pythonCaller.CallClassMethod("MainWrapper", "runFacialRecognition", arguments);
        }

        public static IDictionary<string, string> RecognizeEmotions(string imagePath)
        {
            var arguments = new PythonCallerArgs()
                .AddArgument("imagePath", imagePath);
            return _pythonCaller.CallClassMethod("MainWrapper", "runEmotionDetection", arguments);
        }
    }
}