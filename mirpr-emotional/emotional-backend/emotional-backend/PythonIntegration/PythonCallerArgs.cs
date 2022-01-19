using System;
using System.Collections.Generic;
using Newtonsoft.Json;

namespace emotional_backend.PythonIntegration
{
    public class PythonCallerArgs
    {
        private readonly Dictionary<string, object> _modelArgs;
        private readonly Dictionary<string, object> _metaArgs;
        private readonly JsonSerializerSettings _jsonSettings;

        public PythonCallerArgs()
        {
            _modelArgs = new Dictionary<string, object>();
            _metaArgs = new Dictionary<string, object>();
            _jsonSettings = new JsonSerializerSettings {StringEscapeHandling = StringEscapeHandling.EscapeHtml};
        }
        
        public PythonCallerArgs AddMetaArgument(string property, object obj)
        {
            //Convert each argument to json to keep all consistently
            _metaArgs.Add(JsonConvert.SerializeObject(property, _jsonSettings), JsonConvert.SerializeObject(obj, _jsonSettings));
            return this;
        }
        
        public PythonCallerArgs AddArgument(string name, object obj)
        {
            _modelArgs.Add(name, obj);
            return this;
        }
        
        public string Serialized()
        {
            //AddMetaArgument("date", DateTime.Now);
            AddMetaArgument("modelInput", _modelArgs);
            var res = JsonConvert.SerializeObject(_metaArgs);
            return res;
        }
    }
}