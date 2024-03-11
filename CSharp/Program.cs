// See https://aka.ms/new-console-template for more information
global using eBEST.OpenApi.Models;
using CSharp;

await new _01().Main();

// 샘플 클래스 실행, 무한반복
while (true)
{
    // 샘플 넘버 입력
    ConsoleColor dftForeColor = Console.ForegroundColor;
    Console.ForegroundColor = ConsoleColor.DarkGreen;
    Console.WriteLine();
    Console.Write("샘플넘버 입력(02~): ");
    var input = Console.ReadLine();
    Console.ForegroundColor = dftForeColor;

    if (string.IsNullOrEmpty(input)) continue;
    int.TryParse(input, out var number);
    if (number == 0) continue;

    // 샘플 클래스 찾기
    var type = Type.GetType($"CSharp._{number:00}");
    if (type == null)
    {
        Console.WriteLine("잘못된 샘플넘버 입니다.");
        continue;
    }

    // 샘플 클래스 실행
    await ((SampleBase)Activator.CreateInstance(type)!).ActionImplement();
}
