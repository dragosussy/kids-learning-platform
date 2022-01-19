using System;
using System.Linq;
using System.Threading.Tasks;
using emotional_backend.DbContext;
using emotional_backend.DTOs;
using emotional_backend.Utilities;
using emotional_backend.Utilities.CsvLogger;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;

namespace emotional_backend.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class FaceRecognitionController : ControllerBase
    {
        private readonly ILogger<LoginController> _logger;
        private readonly CsvWriter _csvWriter;
        private readonly Repository _repository;

        public FaceRecognitionController(ILogger<LoginController> logger, Repository repository)
        {
            _logger = logger;
            _repository = repository;
            _csvWriter = new CsvWriter("./emotions-data.csv");
        }

        [HttpPost("recognize-emotions"), DisableRequestSizeLimit]
        public async Task<IActionResult> RecognizeEmotions([FromForm] IFormFile file, [FromForm] string activity, [FromForm] string sessionToken)
        {
            var currentImageGuid = Guid.NewGuid().ToString();
            ImageTools.SaveTemporaryImage(file, currentImageGuid, "./temp_emotion_recog_images");
            //ImageTools.SaveTemporaryImage(file);

            // apelam python
            var imagePath =
                $"E:\\Informatique\\University\\Anul3\\MIRPR\\mirpr-emotional\\emotional-backend\\emotional-backend\\temp_emotion_recog_images\\test{currentImageGuid}.jpg";

            try
            {
                var result = AiTools.RecognizeEmotions(imagePath);
                result.TryGetValue("emotion", out var emotion);

                var userId = (await _repository.Sessions.FirstOrDefaultAsync(s => s.Token == sessionToken))?.UserId;
                var user = await _repository.Users.FirstOrDefaultAsync(u => u.Id == userId);

                if(!string.IsNullOrEmpty(user?.Name) && !string.IsNullOrEmpty(user?.Surname))
                    _csvWriter.Write(new UserEmotion
                    {
                        Emotion = emotion,
                        Activity = activity,
                        TimeRecorded = DateTime.Now,
                        UserName = user?.Name + " " + user?.Surname
                    });

                ImageTools.DeleteTemporaryImage($"test{currentImageGuid}.jpg", "./temp_emotion_recog_images");

                return StatusCode(StatusCodes.Status200OK, emotion);
            }
            catch (Exception e)
            {
                return StatusCode(StatusCodes.Status400BadRequest, e.Message);
            }
        }
    }
}