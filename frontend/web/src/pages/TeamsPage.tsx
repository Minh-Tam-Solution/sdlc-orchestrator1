/**
 * =========================================================================
 * TeamsPage - Teams List and Management
 * SDLC Orchestrator - Sprint 72 Day 2
 *
 * Version: 1.0.0
 * Date: January 28, 2026
 * Status: ACTIVE - Sprint 72 Teams Frontend
 * Authority: Frontend Lead + CTO Approved
 *
 * Purpose:
 * - Display user's teams in responsive grid
 * - Search and filter teams
 * - Create new teams
 * - Navigate to team detail pages
 *
 * SASE Compliance:
 * - SE4H (Human Coach): Can create/manage teams
 * - SE4A (AI Agent): Read-only view of assigned teams
 * =========================================================================
 */

import { useState } from "react";
import { Link } from "react-router-dom";
import { Plus, Search, Users, Folder, UserIcon } from "lucide-react";
import { useTeams } from "@/hooks/useTeams";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import CreateTeamDialog from "@/components/teams/CreateTeamDialog";

/**
 * Teams List Page
 * Shows all teams user is a member of with search and create functionality
 */
export default function TeamsPage() {
  const { data: teams, isLoading } = useTeams();
  const [search, setSearch] = useState("");
  const [showCreateDialog, setShowCreateDialog] = useState(false);

  // Filter teams by search query
  const filteredTeams = teams?.filter((team) =>
    team.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="container mx-auto py-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Teams</h1>
          <p className="text-muted-foreground mt-1">
            Manage your teams and collaborate with your organization
          </p>
        </div>
        <Button onClick={() => setShowCreateDialog(true)}>
          <Plus className="w-4 h-4 mr-2" />
          Create Team
        </Button>
      </div>

      {/* Search Bar */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
        <Input
          placeholder="Search teams..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="pl-10"
        />
      </div>

      {/* Teams Grid */}
      {isLoading ? (
        <TeamsLoadingSkeleton />
      ) : filteredTeams?.length === 0 ? (
        <EmptyState
          hasSearch={search.length > 0}
          onCreateClick={() => setShowCreateDialog(true)}
        />
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {filteredTeams?.map((team) => (
            <TeamCard key={team.id} team={team} />
          ))}
        </div>
      )}

      {/* Create Team Dialog */}
      <CreateTeamDialog
        open={showCreateDialog}
        onOpenChange={setShowCreateDialog}
      />
    </div>
  );
}

/**
 * Team Card Component
 * Displays team summary with members and projects count
 */
interface TeamCardProps {
  team: {
    id: string;
    name: string;
    slug: string;
    description?: string;
    settings: {
      sase_config?: {
        agentic_maturity?: string;
      };
    };
  };
}

function TeamCard({ team }: TeamCardProps) {
  const agenticMaturity = team.settings.sase_config?.agentic_maturity || "L0";

  return (
    <Link to={`/teams/${team.id}`} className="block h-full">
      <Card className="h-full hover:shadow-md transition-shadow cursor-pointer">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex-1 min-w-0">
              <CardTitle className="truncate">{team.name}</CardTitle>
              <CardDescription className="mt-1 truncate">
                @{team.slug}
              </CardDescription>
            </div>
            <Badge variant="outline" className="ml-2 shrink-0">
              {agenticMaturity}
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {team.description && (
            <p className="text-sm text-muted-foreground line-clamp-2">
              {team.description}
            </p>
          )}

          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-1.5">
              <UserIcon className="w-4 h-4" />
              <span>0 members</span>
            </div>
            <div className="flex items-center gap-1.5">
              <Folder className="w-4 h-4" />
              <span>0 projects</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}

/**
 * Empty State Component
 * Shows when no teams exist or search returns no results
 */
interface EmptyStateProps {
  hasSearch: boolean;
  onCreateClick: () => void;
}

function EmptyState({ hasSearch, onCreateClick }: EmptyStateProps) {
  if (hasSearch) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-center">
        <Search className="w-12 h-12 text-muted-foreground mb-4" />
        <h3 className="text-lg font-medium mb-2">No teams found</h3>
        <p className="text-muted-foreground mb-4 max-w-md">
          No teams match your search. Try a different search term or create a
          new team.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <div className="rounded-full bg-muted p-4 mb-4">
        <Users className="w-12 h-12 text-muted-foreground" />
      </div>
      <h3 className="text-lg font-medium mb-2">No teams yet</h3>
      <p className="text-muted-foreground mb-6 max-w-md">
        Create your first team to start collaborating with your organization.
        Teams help organize projects and manage member access.
      </p>
      <Button onClick={onCreateClick}>
        <Plus className="w-4 h-4 mr-2" />
        Create your first team
      </Button>
    </div>
  );
}

/**
 * Loading Skeleton Component
 * Shows while teams data is loading
 */
function TeamsLoadingSkeleton() {
  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {[1, 2, 3, 4, 5, 6].map((i) => (
        <Card key={i}>
          <CardHeader>
            <Skeleton className="h-6 w-3/4 mb-2" />
            <Skeleton className="h-4 w-1/2" />
          </CardHeader>
          <CardContent className="space-y-4">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-full" />
            <div className="flex items-center gap-4">
              <Skeleton className="h-4 w-20" />
              <Skeleton className="h-4 w-20" />
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
