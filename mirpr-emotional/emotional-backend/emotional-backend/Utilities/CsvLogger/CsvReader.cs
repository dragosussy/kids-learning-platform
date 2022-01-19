using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using emotional_backend.DTOs;

namespace emotional_backend.Utilities.CsvLogger
{
    public class CsvReader
    {
        private readonly string _path;

        public CsvReader(string csvFilePath)
        {
            _path = csvFilePath;
        }

        public List<UserEmotion> Read()
        {
            using (var reader = new StreamReader(_path))
            using (var csv = new CsvHelper.CsvReader(reader, CultureInfo.InvariantCulture))
            {
                return csv.GetRecords<UserEmotion>().ToList();
            }
        }
    }
}
