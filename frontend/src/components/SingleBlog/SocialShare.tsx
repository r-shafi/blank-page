
import React from "react";
import { Facebook, Twitter, Linkedin, Link2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";

interface SocialShareProps {
  title: string;
  url: string;
}

const SocialShare: React.FC<SocialShareProps> = ({ title, url }) => {
  const { toast } = useToast();

  const handleShare = (platform: string) => {
    console.log(`Sharing to ${platform}:`, { title, url });
    
    toast({
      title: "Shared!",
      description: `Article has been shared to ${platform}`,
    });
  };

  const handleCopyLink = () => {
    navigator.clipboard.writeText(url);
    console.log("Link copied to clipboard:", url);
    
    toast({
      title: "Link Copied",
      description: "Article link has been copied to clipboard",
    });
  };

  return (
    <div className="flex flex-wrap gap-3">
      <Button
        variant="outline"
        size="sm"
        className="flex items-center gap-2 bg-[#1877F2] text-white hover:bg-[#1877F2]/90 border-none"
        onClick={() => handleShare("Facebook")}
      >
        <Facebook size={16} />
        <span className="hidden sm:inline">Facebook</span>
      </Button>
      
      <Button
        variant="outline"
        size="sm"
        className="flex items-center gap-2 bg-[#1DA1F2] text-white hover:bg-[#1DA1F2]/90 border-none"
        onClick={() => handleShare("Twitter")}
      >
        <Twitter size={16} />
        <span className="hidden sm:inline">Twitter</span>
      </Button>
      
      <Button
        variant="outline"
        size="sm"
        className="flex items-center gap-2 bg-[#0A66C2] text-white hover:bg-[#0A66C2]/90 border-none"
        onClick={() => handleShare("LinkedIn")}
      >
        <Linkedin size={16} />
        <span className="hidden sm:inline">LinkedIn</span>
      </Button>
      
      <Button
        variant="outline"
        size="sm"
        onClick={handleCopyLink}
      >
        <Link2 size={16} className="mr-2" />
        <span>Copy Link</span>
      </Button>
    </div>
  );
};

export default SocialShare;
