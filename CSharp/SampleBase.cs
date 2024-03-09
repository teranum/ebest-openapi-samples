using ConsoleTables;
using eBEST.OpenApi;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace CSharp
{
    internal abstract class SampleBase
    {
        // Api 객체선언
        public static EBestOpenApi api = new();

        // Main: 로그인 및 구현부 호출
        public async Task Main()
        {
            // 로그인
            if (!await api.ConnectAsync(Secret.AppKey, Secret.AppSecretKey))
            {
                print($"연결실패: {api.LastErrorMessage}");
                return;
            }
            print($"연결성공, 접속서버: {(api.ServerType == EBestOpenApi.SERVER_TYPE.모의투자 ? "모의투자" : "실투자")}");

            // 구현부 호출
            await ActionImplement();
        }

        // 구현부: 파생 클래스에서 구현
        public abstract Task ActionImplement();


        // Helper Methods, Properties: print, GetInputAsync, _jsonOptions
        protected static JsonSerializerOptions _jsonOptions = new() { NumberHandling = JsonNumberHandling.AllowReadingFromString };

        public static void print<T>(IEnumerable<T>? array)
        {
            if (array == null) return;
            if (array is string text)
            {
                Console.WriteLine(text);
                return;
            }

            var type = array.GetType().GetElementType()!;
            ConsoleColor dftForeColor = Console.ForegroundColor;
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            Console.WriteLine($"{type.Name}[], Field Count = {type.GetProperties().Length}, Data Count = {array.Count()}");
            Console.ForegroundColor = dftForeColor;
            ConsoleTable.From(array).Configure(o => o.NumberAlignment = Alignment.Right).Write(Format.MarkDown);
        }

        public static void print(object? data)
        {
            if (data is string text)
            {
                Console.WriteLine(text);
                return;
            }
            if (data == null) return;
            List<KeyValuePair<string, object>> keyValuePairs = [];
            var type = data.GetType();
            foreach (var prop in type.GetProperties())
            {
                keyValuePairs.Add(new(prop.Name, prop.GetValue(data) ?? string.Empty));
            }

            ConsoleColor dftForeColor = Console.ForegroundColor;
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            Console.WriteLine($"{type.Name}, Field Count = {keyValuePairs.Count}");
            Console.ForegroundColor = dftForeColor;
            ConsoleTable.From(keyValuePairs).Write(Format.MarkDown);
        }

        public static async Task<string> GetInputAsync(string msg) => await Task.Run(() =>
        {
            Console.Write(msg);
            return Console.ReadLine() ?? string.Empty;
        });
    }
}
