> [!WARNING]  
> I'm really not sure I'm going to pursue this to completion, I'm publishing this "as is" for now

This is a wip rust rewrite of the ink stroke format code using the following references

- the .NET source code viewer
here : https://source.dot.net/#PresentationCore/MS/Internal/Ink/InkSerializedFormat/InkSerializer.cs,127 I'm not sure what's the license is on this though. For reference only ? open promise only ?

This is actually part of https://github.com/dotnet/wpf. And you can effectively open binary isf file using wpf and following https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/storing-ink?view=netframeworkdesktop-4.8. Now one could say
- Maybe we can extract only what we need from this (take a subset of the C# code that only includes the serializer/deserializer part and use that directly or repackage it, to wasm or use any other method to be able to use it in other languages). This doesn't seem easy (also the latest is on .Net 10 beta !!)
- Maybe we can compile the PresentationCore and add debug traces. This way we can compare tag by tag what the reference give us and what we get. Following https://github.com/dotnet/wpf/blob/main/Documentation/developer-guide.md or https://github.com/dotnet/wpf/wiki/Building-WPF-Locally, I've yet to see it build.

- There is also the libisfqt library we can take inspiration from https://gitlab.com/kmess/libisf-qt/-/tree/master?ref_type=heads or https://github.com/blu-base/libisf-qt
- The official ink serialized format specification can be found here  https://www.loc.gov/preservation/digital/formats/digformatspecs/InkSerializedFormat(ISF)Specification.pdf
