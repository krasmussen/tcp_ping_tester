This was a script I wrote in 2014 or 2015 that I ran on an origional Raspberry Pi I had laying around to prove to Cox Communications that their network was having intermitent issues.
Eventually I got the graphite data infront of some higher ups who tasked a team with looking into the issue which was eventually found and corrected.

As this was running on a Raspberry Pi using a slow SD card I found I had issues if I tried to write too much data too frequently so I had to limit how many hosts I was testing against.
Which is why there are so many commented out bits in the code...

Also this was written quickly and a long time ago so I don't feel super proud of it now but it worked well enough at the time.

I'm only committing this to github now because I was thinking about rebuilding this after running into some similar Cox Communication network issues again tonight.

However I figure I'll give them a few days to see if they address the issue on their own, if not I'll go through normal support channels, and if again I get told that what I am experiencing is "ICMP Deprioritization" when I'm logging TCP handshake times I'll probably reach out to contacts I have with Cox Communications to get things addressed again.

Maybe if I rebuild this I might toss it in a container for others to use as well when they experience similar issues.
