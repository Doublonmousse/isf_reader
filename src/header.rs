use std::fs::File;
use std::io::{BufReader, Read, Seek, SeekFrom};
/// utilities for header tests

pub fn header_equality(stream: &mut BufReader<File>, header: Vec<u8>) -> bool {
    let start_position = stream.stream_position().unwrap();

    let header_eq = stream
        .bytes()
        .zip(&header)
        .take(header.len())
        .fold(true, |acc, (l, r)| acc && l.is_ok() && l.unwrap() == *r);
    // reset position
    stream.seek(SeekFrom::Start(start_position)).unwrap();

    return header_eq;
}

pub fn is_base_64_data(stream: &mut BufReader<File>) -> bool {
    let header: Vec<u8> = vec![b'b', b'a', b's', b'e', b'6', b'4', b':'];
    header_equality(stream, header)
}

pub fn is_gif(stream: &mut BufReader<File>) -> bool {
    let header: Vec<u8> = vec!['G', 'I', 'F'].into_iter().map(|c| c as u8).collect();
    header_equality(stream, header)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_b64() {
        let mut my_buf: BufReader<File> =
            BufReader::new(File::open("./files_test/638692041872379392.gif").unwrap());
        assert!(is_base_64_data(&mut my_buf) == false)
    }

    #[test]
    fn test_gif() {
        let mut my_buf: BufReader<File> =
            BufReader::new(File::open("./files_test/638692041872379392.gif").unwrap());
        assert!(is_gif(&mut my_buf) == true)
    }

}