using System;

namespace emotional_backend.DTOs
{
    public class UserEmotion
    {
        public string UserName { get; set; }
        public string Emotion { get; set; }
        public string Activity { get; set; }
        public DateTime TimeRecorded { get; set; }

        public string ToCsv()
        {
            return $"{UserName},{Emotion},{Activity},{TimeRecorded}";
        }
    }
}