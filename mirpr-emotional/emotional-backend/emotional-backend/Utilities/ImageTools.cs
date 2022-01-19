using System.IO;
using Microsoft.AspNetCore.Http;

namespace emotional_backend.Utilities
{
    public static class ImageTools
    {
        public static void SaveTemporaryImage(IFormFile file, string fileId = "", string folderPath = "./temp_auth_images")
        {
            folderPath = folderPath.TrimEnd('/');
            
            using (var memoryStream = new MemoryStream())
            {
                file.CopyTo(memoryStream);
                using (FileStream filestream = new FileStream($"{folderPath}/test{fileId}.jpg", FileMode.Create, FileAccess.Write))
                    memoryStream.WriteTo(filestream);
            }
        }
        
        public static void DeleteTemporaryImage(string fileName, string folderPath = "./temp_auth_images")
        {
            folderPath = folderPath.TrimEnd('/');
            
            var fullPathToImage = $"{folderPath}/{fileName}";
            
            if(File.Exists(fullPathToImage))
                File.Delete(fullPathToImage);
        }
    }
}