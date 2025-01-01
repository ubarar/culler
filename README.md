# culler

### Demo

[![Watch Demo](/demo.mp4))](/demo.mp4)

### Why?

You have a great day shooting with your Sony™️ Mirrorless Camera, and you come home to find about 500 shots on your SD card. Each file is around 400mb, so you've managed to shoot 20gb of photos in one day.

When you open the directory containing the images in Finder, it completely freezes up and you wait for minutes to just see a few previews. So you choose to open these photos in Lightrooms import feature, which thankfully is much faster. However, lightroom only allows you to view your images in tiny 200px boxes before you choose to import them.

Like me, you may not want to clutter Lightroom with hundreds of throwaway shots, nor do you want to fill up your archives with tons of junk. Like me, you need a good way to delete files _from your storage_ medium that happens to be blazing fast.

### Technical Point

Sony's ARW files come embedded with a JPEG preview. This is the file your camera body shows you when you're looking at a shot, and this is the image that contains your DRO-corrected image if you happen to use it.

This program simply pulls up that embedded image in a big window to help you decide what to do.

### On Code quality

The code-quality here is awful. I wrote this on new years eve knowing nothing about Qt whatsoever. Half the code is from ChatGPT, and the other half is shamelessly stolen from [this repo](https://github.com/WowkDigital/arw_to_jpg_UI). I ask for forgiveness 🙏