import { Users, Building, MapPin, Calendar, Network } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Entity, Relationship } from '@/types/market';
import { cn } from '@/lib/utils';

interface EntityPanelProps {
  entities: Entity[];
  relationships: Relationship[];
}

const entityConfig = {
  person: {
    icon: Users,
    color: 'text-chart-1',
    bg: 'bg-chart-1/10',
  },
  organization: {
    icon: Building,
    color: 'text-chart-2',
    bg: 'bg-chart-2/10',
  },
  location: {
    icon: MapPin,
    color: 'text-chart-4',
    bg: 'bg-chart-4/10',
  },
  event: {
    icon: Calendar,
    color: 'text-chart-5',
    bg: 'bg-chart-5/10',
  },
};

export function EntityPanel({ entities, relationships }: EntityPanelProps) {
  const sortedEntities = [...entities].sort((a, b) => b.mentions - a.mentions);

  return (
    <Card className="glass-card h-full">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          <Network className="h-5 w-5 text-primary" />
          Entities & Relationships
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div>
            <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-3">
              Key Entities ({entities.length})
            </h4>
            <ScrollArea className="h-[180px] scrollbar-thin">
              <div className="space-y-2">
                {sortedEntities.map((entity) => {
                  const config = entityConfig[entity.type];
                  const Icon = config.icon;
                  const maxMentions = Math.max(...entities.map((e) => e.mentions));
                  const barWidth = (entity.mentions / maxMentions) * 100;

                  return (
                    <div key={entity.id} className="flex items-center gap-3 group">
                      <div className={cn("flex h-7 w-7 shrink-0 items-center justify-center rounded", config.bg)}>
                        <Icon className={cn("h-3.5 w-3.5", config.color)} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-sm font-medium truncate">{entity.name}</span>
                          <span className="text-xs text-muted-foreground">{entity.mentions}</span>
                        </div>
                        <div className="h-1 bg-muted rounded-full overflow-hidden">
                          <div
                            className={cn("h-full rounded-full transition-all", config.bg.replace('/10', ''))}
                            style={{ width: `${barWidth}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </ScrollArea>
          </div>

          <div>
            <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-3">
              Relationships ({relationships.length})
            </h4>
            <ScrollArea className="h-[100px] scrollbar-thin">
              <div className="space-y-2">
                {relationships.map((rel, idx) => {
                  const source = entities.find((e) => e.id === rel.sourceId);
                  const target = entities.find((e) => e.id === rel.targetId);

                  return (
                    <div key={idx} className="flex items-center gap-2 text-sm">
                      <Badge variant="secondary" className="text-xs">
                        {source?.name}
                      </Badge>
                      <span className="text-muted-foreground">→</span>
                      <Badge variant="outline" className="text-xs">
                        {rel.type.replace('_', ' ')}
                      </Badge>
                      <span className="text-muted-foreground">→</span>
                      <Badge variant="secondary" className="text-xs">
                        {target?.name}
                      </Badge>
                    </div>
                  );
                })}
              </div>
            </ScrollArea>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
