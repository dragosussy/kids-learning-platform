using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using emotional_backend.DbContext;
using emotional_backend.DTOs;
using emotional_backend.Models;
using emotional_backend.Utilities.CsvLogger;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace emotional_backend.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class DataController : ControllerBase
    {
        private readonly CsvReader _csvReader;
        private readonly Repository _repository;

        public DataController(Repository repository)
        {
            _repository = repository;
            _csvReader = new CsvReader("./emotions-data.csv");
        }

        [HttpGet("emotions")]
        public List<UserEmotion> GetEmotionsSummary(string userName = "")
        {
            return _csvReader.Read();
        }

        [HttpGet("all-users")]
        public async Task<List<User>> GetUsers()
        {
            return await _repository.Users.ToListAsync();
        }

        [HttpGet("daily-report")]
        public DailyEmotionsReportDto GetDailyReport(DateTime? date, string username)
        {
            if(date == null) date = DateTime.Now;

            var emotions = _csvReader.Read();

            var summary = new DailyEmotionsReportDto() {Emotions = new Dictionary<DateTime, string>()};

            foreach (var userEmotion in emotions)
            {
                if (date?.Date.CompareTo(userEmotion.TimeRecorded.Date) != 0 || userEmotion.UserName != username) continue;

                summary.Emotions.Add(userEmotion.TimeRecorded, userEmotion.Emotion);
            }

            return summary;
        }
    }
}
