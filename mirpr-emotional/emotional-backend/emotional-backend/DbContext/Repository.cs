using emotional_backend.Models;
using Microsoft.EntityFrameworkCore;

namespace emotional_backend.DbContext
{
    public class Repository : Microsoft.EntityFrameworkCore.DbContext
    {
        public DbSet<User> Users { get; set; }
        public DbSet<Session> Sessions { get; set; }
        public DbSet<AdminUser> AdminUsers { get; set; }

        public Repository(string connectionString) : base(GetOptions(connectionString))
        {
        }

        private static DbContextOptions GetOptions(string connectionString)
        {
            return new DbContextOptionsBuilder().UseSqlServer(connectionString).Options;
        }
    }
}