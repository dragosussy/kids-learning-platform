using CsvHelper.Configuration;
using emotional_backend.DTOs;

namespace emotional_backend.Utilities.CsvLogger.Mappers
{
    public sealed class UserEmotionMapper : ClassMap<UserEmotion>
    {
        public UserEmotionMapper()
        {
            Map(x => x.UserName).Name("UserName");
            Map(x => x.Emotion).Name("Emotion");
            Map(x => x.Activity).Name("Activity");
            Map(x => x.TimeRecorded).Name("TimeRecorded");
        }
    }
}