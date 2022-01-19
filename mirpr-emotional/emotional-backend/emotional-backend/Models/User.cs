using System.ComponentModel.DataAnnotations;

namespace emotional_backend.Models
{
    public class User
    {
        [Key]
        public int Id { get; set; }
        
        public string Name { get; set; }
        
        public string Surname { get; set; }
    }
}