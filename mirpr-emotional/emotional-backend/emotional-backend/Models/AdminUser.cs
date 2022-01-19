using System.ComponentModel.DataAnnotations;

namespace emotional_backend.Models
{
    public class AdminUser
    {
        [Key]
        public int Id { get; set; }

        public string UserName { get; set; }

        public string Password { get; set; }
    }
}
