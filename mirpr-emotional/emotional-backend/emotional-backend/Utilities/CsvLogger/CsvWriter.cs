using System.Globalization;
using System.IO;
using CsvHelper.Configuration;
using emotional_backend.DTOs;

namespace emotional_backend.Utilities.CsvLogger
{
    public class CsvWriter
    {
        private readonly string _path;

        private readonly CsvConfiguration _config = new CsvConfiguration(CultureInfo.InvariantCulture)
            { HasHeaderRecord = false };
        
        public CsvWriter(string csvFilePath)
        {
            _path = csvFilePath;
        }

        public void Write(UserEmotion emotionData)
        {
            using (var stream = File.Open(_path, FileMode.Append))
            using (var writer = new StreamWriter(stream))
            using (var csv = new CsvHelper.CsvWriter(writer, _config))
            {
                csv.WriteField(emotionData.ToCsv(), shouldQuote: false);
                csv.NextRecordAsync();
            }
        }
    }
}