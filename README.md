# TODO:

- Add mIRC support
- Color formatting for HexChat
- Configurable options
  - Color options
  - Channel limit options
  - Callout limit options
- Calculate multiple sctimes in a single line
- Some sort of gravwell support
- Organize Adi into separate functions

# Limitations:

Purposeful:
Mecha is ignored
Distances in light years is ignored over 0.5ly

Unintentional:
Historic logs when launching a client might print incorrect (now) timestamps for lines with distances in them

Adi:
Only calculates right-most distance in a message
Only messages from other users
Does not support DMs

HexChat:
Only calculates left-most distance in a message
Supports self and channel messages
Does not support DMs