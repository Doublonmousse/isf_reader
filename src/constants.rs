// contains all hardcoded values for constants, tags, guids etc...

pub(crate) const TAG_INK_SPACE_RECT: u64 = 0;
/// Seems to be for custom properties only ?
/// For now this tag is skipped (read then skip reading the data)
pub(crate) const TAG_GUID_TABLE: u64 = 1;
pub(crate) const TAG_DRAW_ATTRS_TABLE: u64 = 2;
pub(crate) const TAG_DRAW_ATTRS_BLOCK: u64 = 3;
pub(crate) const TAG_STROKE_DESC_TABLE: u64 = 4;
pub(crate) const TAG_STROKE_DESC_BLOCK: u64 = 5;
pub(crate) const TAG_BUTTONS: u64 = 6;
pub(crate) const TAG_NO_X: u64 = 7;
pub(crate) const TAG_NO_Y: u64 = 8;
pub(crate) const TAG_DIDX: u64 = 9;
pub(crate) const TAG_STROKE: u64 = 10;
pub(crate) const TAG_STROKE_PROPERTY_LIST: u64 = 11;
pub(crate) const TAG_POINT_PROPERTY:u64 = 12;
pub(crate) const TAG_SIDX:u64 = 13;
pub(crate) const TAG_COMPRESSION_HEADER:u64 = 14;
pub(crate) const TAG_TRANSFORM_TABLE:u64 = 15;
pub(crate) const TAG_TRANSFORM:u64 = 16;
pub(crate) const TAG_TRANSFORM_ISOTROPIC_SCALE:u64 = 17;
pub(crate) const TAG_TRANSFORM_ANISOTROPIC_SCALE:u64 = 18;
pub(crate) const TAG_TRANSFORM_ROTATE:u64 = 19;
pub(crate) const TAG_TRANSFORM_TRANSLATE:u64 = 20;
pub(crate) const TAG_TRANSFORM_SCALE_AND_TRANSLATE:u64 = 21;
pub(crate) const TAG_TRANSFORM_QUAD:u64 = 22;
pub(crate) const TAG_TIDX:u64 = 23;
pub(crate) const TAG_METRIC_TABLE:u64 = 24;
pub(crate) const TAG_METRIC_BLOCK:u64 = 25;
pub(crate) const TAG_MIDX:u64 = 26;
pub(crate) const TAG_MANTISSA:u64 = 27;
pub(crate) const TAG_PERSISTENT_FORMAT:u64 = 28;
// parsed but not used for now...
pub(crate) const TAG_HIMETRIC_SIZE:u64 = 29;
pub(crate) const TAG_STROKE_IDS:u64 = 30;