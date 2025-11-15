/// for now we will just read it and print it then move on
/// Will do proper typing later when guuid start to serve a
/// purpose
pub(crate) fn decode_guid(bytes: [u8; 16]) {
    // guid structure :

    // in binary
    // uint (32 bits hence 4 bytes)
    let tag: u32 = (bytes[0] as u32) << 24
        | ((bytes[1] as u32) << 16)
        | ((bytes[2] as u32) << 8)
        | (bytes[3] as u32);

    // ushort (16 bites hence 2 bytes)
    let b1: u16 = (bytes[4] as u16) << 8 | bytes[5] as u16;
    // ushort (16 bits hence 2 bytes)
    let b2: u16 = (bytes[6] as u16) << 8 | bytes[7] as u16;
    // 8 bytes (saved in 8 different fields -> char list)
    let ch_list = &bytes[8..];

    // print
    println!("guid : \t{:?}\t{:?}\t{:?}\t{:?}", tag, b1, b2, ch_list);

    // parse and check later the use ...
    // to check later when we'd have associated values with this
}
