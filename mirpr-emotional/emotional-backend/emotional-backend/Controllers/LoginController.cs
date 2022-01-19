using System;
using System.Linq;
using System.Security.Cryptography;
using emotional_backend.DbContext;
using emotional_backend.Models;
using emotional_backend.Utilities;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace emotional_backend.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class LoginController : ControllerBase
    {
        private readonly ILogger<LoginController> _logger;
        private readonly Repository _repository;

        public LoginController(ILogger<LoginController> logger, Repository repository)
        {
            _logger = logger;
            _repository = repository;
        }

        [HttpPost("login"), DisableRequestSizeLimit]
        public IActionResult Login([FromForm] IFormFile file, [FromForm] string loggedInToken = "")
        {
            try
            {
                // User is already logged in
                Session userSession = null;
                if (!string.IsNullOrEmpty(loggedInToken))
                    userSession = _repository.Sessions.FirstOrDefault(s => s.Token == loggedInToken);
                if (userSession != null)
                    return StatusCode(StatusCodes.Status200OK, loggedInToken);
                if (!string.IsNullOrEmpty(loggedInToken))
                    return StatusCode(StatusCodes.Status200OK, loggedInToken);
                
                if (file == null)
                    return StatusCode(StatusCodes.Status400BadRequest, "No image was sent.");

                ImageTools.SaveTemporaryImage(file);
                
                // apelam python
                var imagePath =
                    "E:\\Informatique\\University\\Anul3\\MIRPR\\mirpr-emotional\\emotional-backend\\emotional-backend\\temp_auth_images\\test.jpg";
                var resultDict = AiTools.RecognizeFace(imagePath);

                if (resultDict == null)
                    return StatusCode(StatusCodes.Status403Forbidden, "Login already performed.");

                resultDict.TryGetValue("name", out var recognizedPersonName);
                var user = _repository.Users.FirstOrDefault(u => recognizedPersonName.ToLower() == (u.Surname + u.Name).ToLower());
                if (user == null)
                    return StatusCode(StatusCodes.Status401Unauthorized, $"Nu ne place fata ta, {recognizedPersonName}.");
                
                
                ImageTools.DeleteTemporaryImage("test.jpg");
                
                var sessionToken = Guid.NewGuid();

                // replace user Id with the one matching user's face
                _repository.Sessions.Add(new Session { Token = sessionToken.ToString(), UserId = user.Id });
                _repository.SaveChanges();
                
                return StatusCode(StatusCodes.Status200OK, sessionToken.ToString());
            }
            catch (Exception e)
            {
                return StatusCode(StatusCodes.Status500InternalServerError, e.Message);
            }
        }

        [HttpPost("admin-login"), DisableRequestSizeLimit]
        public IActionResult AdminLogin([FromForm] string username, [FromForm] string password)
        {
            var user = _repository.AdminUsers.FirstOrDefault(u => u.UserName == username);
            if (user == null) return StatusCode(StatusCodes.Status403Forbidden, "Invalid user.");

            var hashedPassword = password.ApplySha256();
            if(!hashedPassword.Equals(user.Password, StringComparison.InvariantCultureIgnoreCase))
                return StatusCode(StatusCodes.Status403Forbidden, "Invalid password.");

            return StatusCode(StatusCodes.Status200OK);
        }
    }
}