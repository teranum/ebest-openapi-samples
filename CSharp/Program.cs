// See https://aka.ms/new-console-template for more information

using ConsoleTables;
using CSharp;
using System.Text.Json;
using System.Text.Json.Serialization;

await _22.Main();

namespace CSharp
{
    public enum CandleGubun
    {
        틱, 분, 일, 주, 월, 년,
    }

    internal class SampleBase
    {
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
            Console.WriteLine($"{type.Name}[], Field Count = {type.GetProperties().Length}, Data Count = {array.Count()}");
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

            Console.WriteLine($"{type.Name}, Field Count = {keyValuePairs.Count}");
            ConsoleTable.From(keyValuePairs).Write(Format.MarkDown);
        }
    }
}
