from gwproto import CallableDecoder
from gwproto import Decoders
from gwproto import MQTTCodec
from gwproto import create_message_payload_discriminator
from gwproto.gs import GsPwr_Maker
from gwproto.gt.gt_dispatch_boolean import GtDispatchBoolean_Maker
from gwproto.gt.gt_sh_cli_atn_cmd import GtShCliAtnCmd_Maker
from gwproto.gt.gt_sh_status import GtShStatus_Maker
from gwproto.gt.snapshot_spaceheat import SnapshotSpaceheat_Maker


S3MessageDecoder = create_message_payload_discriminator(
    "S3MessageDecoder",
    [
        "gwproto.messages",
    ],
)


class S3MQTTCodec(MQTTCodec):
    def __init__(self):
        super().__init__(
            Decoders.from_objects(
                [
                    GtDispatchBoolean_Maker,
                    GtShCliAtnCmd_Maker,
                    GtShStatus_Maker,
                    SnapshotSpaceheat_Maker,
                ],
                message_payload_discriminator=S3MessageDecoder,
            ).add_decoder(
                "p", CallableDecoder(lambda decoded: GsPwr_Maker(decoded[0]).tuple)
            )
        )

    def validate_source_alias(self, source_alias: str):
        pass
