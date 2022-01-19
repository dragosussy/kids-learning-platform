using System;
using System.Collections.Generic;

namespace emotional_backend.DTOs
{
    public class DailyEmotionsReportDto
    {
        public Dictionary<DateTime, string> Emotions { get; set; }
    }
}
