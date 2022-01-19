using System.Security.Cryptography;
using System.Text;

namespace emotional_backend.Utilities
{
    public static class StringExtensions
    {
        public static string ApplySha256(this string input)
        {
            byte[] byteArray;
            using (var hashAlgorithm = SHA256.Create())
            {
                byteArray = hashAlgorithm.ComputeHash(Encoding.UTF8.GetBytes(input));
            }

            var stringBuilder = new StringBuilder();
            foreach (var _byte in byteArray)
            {
                stringBuilder.Append(_byte.ToString("X2"));
            }

            return stringBuilder.ToString();
        }
    }
}
