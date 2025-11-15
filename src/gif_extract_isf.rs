use std::fs::File;
use std::io::{BufReader, Cursor, Read};

use crate::header;

/// Source : https://giflib.sourceforge.net/whatsinagif/bits_and_bytes.html

/// The ISF data is embedded inside the gif as a comment extension block
pub fn get_isf_from_gif(
    stream: &mut BufReader<File>,
) -> Result<BufReader<std::io::Cursor<Vec<u8>>>, ()> {
    stream
        .seek_relative(
            6 + // the GIF89 header (already tested)
        2 + // canvas width
        2, // canvas height
        )
        .unwrap();

    // get the color resolution from the packed logical screen descriptor
    let log_descriptor = stream.bytes().into_iter().next().unwrap().unwrap();
    let color_res: u32 = [
        (log_descriptor & 0b010_0000) != 0,
        (log_descriptor & 0b001_0000) != 0,
        (log_descriptor & 0b000_1000) != 0,
    ]
    .into_iter()
    .zip([4, 2, 1])
    .fold(0, |acc, (bool, value)| if bool { acc + value } else { acc });
    let global_color_table_size: u32 = [
        (log_descriptor & 0b0000_100) != 0,
        (log_descriptor & 0b0000_010) != 0,
        (log_descriptor & 0b0000_001) != 0,
    ]
    .into_iter()
    .zip([4, 2, 1])
    .fold(0, |acc, (bool, value)| if bool { acc + value } else { acc });

    let n_color_table = if global_color_table_size != 0 {
        global_color_table_size
    } else {
        color_res
    };

    stream
        .seek_relative(
            2 + // end of the logical screen descriptor
            3 * 2_i64.pow(n_color_table + 1) + // color table (local or global)
            8 + // graphics color extension (optional but not checked here !)
            10 + // image descriptor
            1, // LZ code
        )
        .unwrap();

    // start of the image data
    // iterate until we have zero (end of block)
    let mut data_size = stream.bytes().next().unwrap().unwrap() as i64;
    while data_size > 0 {
        stream.seek_relative(data_size).unwrap();
        data_size = stream.bytes().next().unwrap().unwrap() as i64;
    }

    // the two next bytes should be the 21 FE for
    // the extension introducer and the comment extension code
    let check_isf_block_start = header::header_equality(stream, vec![0x21, 0xFE]);
    if !check_isf_block_start {
        // we messed up something
        return Err(());
    } else {
        // as we the header eq puts the reader back
        // in the original position, advance by two
        stream.seek_relative(2).unwrap();
    }

    // read the stream
    let mut data_size = stream.bytes().next().unwrap().unwrap() as i64;
    let mut isf_data: Vec<u8> = vec![];
    while data_size > 0 {
        // save to a vec the u8 stream instead for now (maybe not super efficient)
        for el in stream.bytes().take(data_size as usize) {
            isf_data.push(el.unwrap())
        }
        data_size = stream.bytes().next().unwrap().unwrap() as i64;
    }

    // check we are at the end of the block : 3B terminator
    if stream.bytes().next().unwrap().unwrap() != 0x3B {
        Err(())
    } else {
        // wrap our vec to be a BufReader once again
        Ok(BufReader::new(Cursor::new(isf_data)))
    }
}
