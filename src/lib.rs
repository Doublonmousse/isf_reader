mod constants;

mod gif_extract_isf;
mod header;
mod parsers_tags;
mod utils;

use gif_extract_isf::get_isf_from_gif;
use std::fs::File;
use std::io::{BufReader, Error, Read};
use utils::{decode_multibyte_int, decode_multibyte_signed, update_remaining};

pub fn decode_isf(mut stream: BufReader<File>) -> Result<(), Error> {
    let is_b64 = header::is_base_64_data(&mut stream);
    if is_b64 {
        return Err(std::io::ErrorKind::InvalidData.into());
        // not implemented !
    }
    let is_gif = header::is_gif(&mut stream);
    if is_gif {
        match get_isf_from_gif(&mut stream) {
            Ok(stream_raw) => Ok(decode_isf_raw(stream_raw)?),
            Err(()) => Err(std::io::ErrorKind::InvalidData.into()),
        }
    } else {
        Ok(decode_isf_raw(stream)?)
    }
}

pub fn decode_isf_raw<R: Read>(mut stream: BufReader<R>) -> Result<(), Error> {
    // check we start with 0x00
    let first_byte = (&mut stream).bytes().next().unwrap().unwrap();
    if first_byte != 0x00 {
        return Err(std::io::ErrorKind::InvalidData.into());
    } else {
        // get the size of the stream
        let (mut remaining, bytes_read) = decode_multibyte_int(&mut stream)?;

        println!(
            "Size of the stream : {:?}, bytes read: {:?}",
            &remaining, bytes_read
        );

        // loop over blocks
        while remaining > 0 {
            // read the tag
            let (isf_tag, isf_tag_len) = decode_multibyte_int(&mut stream)?;
            update_remaining(&mut remaining, isf_tag_len)?;

            println!("isf tag : {isf_tag}");
            match isf_tag {
                constants::TAG_GUID_TABLE => {
                    let (tag_bytes_length, bytes_read) = decode_multibyte_int(&mut stream)?;
                    // technically equivalent but not checked (if the reader is not correct, this might not be !)
                    update_remaining(&mut remaining, bytes_read + tag_bytes_length)?;

                    // should be a multiple of 16
                    println!(
                        "guid table of size {:?} hence {:?} custom guids",
                        tag_bytes_length,
                        tag_bytes_length / 16
                    );
                    // read chunks of 16
                    for _ in 0..tag_bytes_length / 16 {
                        let mut element: [u8; 16] = [0; 16];
                        (&mut stream).read_exact(&mut element)?;
                        parsers_tags::decode_guid(element);
                    }
                }
                constants::TAG_DRAW_ATTRS_TABLE => {
                    let (mut tag_bytes_length, bytes_read) = decode_multibyte_int(&mut stream)?;
                    // technically equivalent but not checked (if the reader is not correct, this might not be !)
                    update_remaining(&mut remaining, bytes_read + tag_bytes_length)?;

                    while tag_bytes_length > 0 {
                        let (drawing_attribute_length, read_bytes) =
                            decode_multibyte_int(&mut stream)?;
                        // then DrawingAttributeSerializer.DecodeAsISF
                        // FROM DrawingAttributeSerializer (take the right one)
                        // should be a loop on tag_bytes_length decreasing
                        // we check the first value obtained here first
                        let (uiTag, cb) = decode_multibyte_int(&mut stream)?;
                        println!("tag found : {:?}", uiTag);
                        todo!("stop here UB");
                    }

                    // localBytesDecoded = LoadDrawAttrsTable(inputStream, guidList, tag_bytes_length);
                    // stream, guidlist, size of the current block
                    // guidlist not decoded from the last part !
                    // but needed here (?)
                    // drawingAttributesBlockDecoded = true; // bool to signify we already parsed a
                    // draw attr table hence need additional logic when parsing strokes
                    // can't parse strokes if no draw attr found before it

                    todo!("tag draw attr table not implemented")
                }
                constants::TAG_HIMETRIC_SIZE => {
                    let (tag_bytes_length, bytes_read) = decode_multibyte_int(&mut stream)?;
                    // technically equivalent but not checked (if the reader is not correct, this might not be !)
                    update_remaining(&mut remaining, bytes_read + tag_bytes_length)?;

                    let (himetric_size_x, _) = decode_multibyte_signed(&mut stream)?;
                    let (himetric_size_y, _) = decode_multibyte_signed(&mut stream)?;

                    println!("himetric sizes {:?} {:?}", himetric_size_x, himetric_size_y);
                    // used for anything ? apart from having to read the two values ?
                }
                _ => break,
            }
        }

        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_decode() {
        let my_buf: BufReader<File> =
            BufReader::new(File::open("./files_test/638692041872379392.gif").unwrap());
        assert!(decode_isf(my_buf).is_ok());
    }

    #[test]
    fn test_decode_raw() {
        let my_buf: BufReader<File> =
            BufReader::new(File::open("./files_test/binary_isf.txt").unwrap());
        assert!(decode_isf(my_buf).is_ok());
    }
}
