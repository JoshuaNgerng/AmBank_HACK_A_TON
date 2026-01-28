import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { MessageCircle, X } from 'lucide-react';
import { ChatDrawer } from './ChatDrawer';
import { ChatContext } from '@/types/chat';
import { cn } from '@/lib/utils';

interface FloatingChatButtonProps {
  context: ChatContext;
}

export function FloatingChatButton({ context }: FloatingChatButtonProps) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <Button
        onClick={() => setOpen(true)}
        size="lg"
        className={cn(
          'fixed bottom-6 right-6 h-14 w-14 rounded-full shadow-lg z-50',
          'transition-transform hover:scale-105 active:scale-95'
        )}
      >
        {open ? (
          <X className="h-6 w-6" />
        ) : (
          <MessageCircle className="h-6 w-6" />
        )}
      </Button>

      <ChatDrawer open={open} onOpenChange={setOpen} context={context} />
    </>
  );
}
