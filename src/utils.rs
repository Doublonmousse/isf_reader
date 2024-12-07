use std::{
    io::Error,
    io::{BufReader, Read},
};

// helper to read the entire value
fn read_value<R: Read>(stream: &mut BufReader<R>) -> Result<(u64, u64), Error> {
    let mut bytes_read: u64 = 0;
    let mut value: u64 = 0;
    let mut shift: usize = 0;

    loop {
        let next_byte = stream.bytes().next().unwrap()?;
        bytes_read += 1;
        value += ((next_byte & 0b0111_1111) as u64) << shift;
        shift += 7; //shifting the value towards the left

        if (next_byte & 0b1000_0000) == 0 {
            // we need to include everything up to the first bytes with a zero
            // on the most important byte included
            break;
        }
    }
    return Ok((value, bytes_read));
}

/// reads the mulibytes int and returns both the value and the number
/// of bytes read
///
/// We have
/// ```rs
/// let (value, bytes_read) = decode_multibytes_int(&mut stream)?;
/// ```
/// equivalent to
/// ```C#
/// uint bytes_read = SerializationHelper.Decode(strm, out value);
/// ```
pub fn decode_multibyte_int<R: Read>(stream: &mut BufReader<R>) -> Result<(u64, u64), Error> {
    read_value(stream)
}

pub fn decode_multibyte_signed<R: Read>(stream: &mut BufReader<R>) -> Result<(i64, u64), Error> {
    let (value_u, bytes_read) = read_value(stream)?;
    if value_u & 0x01 > 0 {
        return Ok((-((value_u >> 1) as i64), bytes_read));
    } else {
        return Ok(((value_u >> 1) as i64, bytes_read));
    }
}

pub fn update_remaining(remaining: &mut u64, read: u64) -> Result<(), Error> {
    match remaining.checked_sub(read) {
        Some(out) => {
            *remaining = out;
            Ok(())
        }
        None => Err(std::io::ErrorKind::InvalidData.into()),
    }
}

#[cfg(test)]
mod test_utils {
    use crate::gif_extract_isf::get_isf_from_gif;

    use super::*;
    use std::fs::File;

    #[test]
    fn decode_mb() {
        let mut my_buf: BufReader<File> =
            BufReader::new(File::open("./files_test/638692041872379392.gif").unwrap());
        // get isf from raw
        let mut raw_isf = get_isf_from_gif(&mut my_buf).unwrap();

        // skip header
        (&mut raw_isf).bytes().next().unwrap().unwrap();

        let (value, bytes_read) = decode_multibyte_int(&mut raw_isf).unwrap();
        assert_eq!(value, 22760);
        assert_eq!(bytes_read, 3);
    }
}
