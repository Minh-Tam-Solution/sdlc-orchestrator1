/**
 * =========================================================================
 * TeamDetailPage - Team Dashboard and Overview
 * SDLC Orchestrator - Sprint 72 Day 3
 *
 * Version: 1.0.0
 * Date: January 28, 2026
 * Status: ACTIVE - Sprint 72 Teams Frontend
 * Authority: Frontend Lead + CTO Approved
 *
 * Purpose:
 * - Display team overview with statistics
 * - Show team members list
 * - Show recent projects
 * - Quick actions for team management
 *
 * SASE Compliance:
 * - SE4H (Human Coach): Full dashboard access
 * - SE4A (AI Agent): Limited to assigned tasks
 * =========================================================================
 */

import { useParams, Link } from "react-router-dom";
import {
  Users,
  Folder,
  Settings,
  TrendingUp,
  ChevronRight,
} from "lucide-react";
import { useTeam, useTeamStatistics } from "@/hooks/useTeams";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

/**
 * Team Detail Page
 * Shows team dashboard with stats, members, and projects
 */
export default function TeamDetailPage() {
  const { teamId } = useParams<{ teamId: string }>();
  const { data: team, isLoading: teamLoading } = useTeam(teamId || null);
  const { data: stats, isLoading: statsLoading } = useTeamStatistics(
    teamId || null
  );

  if (teamLoading) {
    return <TeamDetailSkeleton />;
  }

  if (!team) {
    return <TeamNotFound />;
  }

  return (
    <div className="container mx-auto py-6 space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div className="space-y-1">
          <h1 className="text-3xl font-bold tracking-tight">{team.name}</h1>
          <p className="text-muted-foreground">@{team.slug}</p>
          {team.description && (
            <p className="text-sm text-muted-foreground mt-2 max-w-2xl">
              {team.description}
            </p>
          )}
        </div>

        <div className="flex items-center gap-2">
          <Link to={`/teams/${teamId}/settings`}>
            <Button variant="outline">
              <Settings className="w-4 h-4 mr-2" />
              Settings
            </Button>
          </Link>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="grid gap-6 md:grid-cols-3">
        <StatCard
          title="Members"
          value={stats?.member_count || 0}
          icon={<Users className="w-4 h-4" />}
          subtext={`${stats?.se4h_count || 0} coaches, ${
            stats?.se4a_count || 0
          } agents`}
          loading={statsLoading}
        />
        <StatCard
          title="Projects"
          value={stats?.project_count || 0}
          icon={<Folder className="w-4 h-4" />}
          subtext={`${stats?.active_projects || 0} active`}
          loading={statsLoading}
        />
        <StatCard
          title="Agentic Maturity"
          value={stats?.agentic_maturity || "L0"}
          icon={<TrendingUp className="w-4 h-4" />}
          subtext="SASE Framework"
          loading={statsLoading}
        />
      </div>

      {/* Content Grid */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Team Members */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-base font-medium">
              Team Members
            </CardTitle>
            <Link to={`/teams/${teamId}/members`}>
              <Button variant="ghost" size="sm">
                View All
                <ChevronRight className="w-4 h-4 ml-1" />
              </Button>
            </Link>
          </CardHeader>
          <CardContent>
            <MembersList members={team.members.slice(0, 5)} />
          </CardContent>
        </Card>

        {/* Recent Projects */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-base font-medium">
              Recent Projects
            </CardTitle>
            <Link to={`/projects?team=${teamId}`}>
              <Button variant="ghost" size="sm">
                View All
                <ChevronRight className="w-4 h-4 ml-1" />
              </Button>
            </Link>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              No projects yet. Create your first project to get started.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

/**
 * Stat Card Component
 */
interface StatCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  subtext: string;
  loading?: boolean;
}

function StatCard({ title, value, icon, subtext, loading }: StatCardProps) {
  if (loading) {
    return (
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <Skeleton className="h-4 w-20" />
          {icon}
        </CardHeader>
        <CardContent>
          <Skeleton className="h-8 w-16 mb-1" />
          <Skeleton className="h-3 w-32" />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {icon}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <p className="text-xs text-muted-foreground mt-1">{subtext}</p>
      </CardContent>
    </Card>
  );
}

/**
 * Members List Component
 */
interface MembersListProps {
  members: Array<{
    id: string;
    role: string;
    member_type: string;
    user?: {
      full_name?: string;
      email: string;
      avatar_url?: string;
    };
  }>;
}

function MembersList({ members }: MembersListProps) {
  if (members.length === 0) {
    return (
      <p className="text-sm text-muted-foreground">
        No members yet. Invite members to start collaborating.
      </p>
    );
  }

  return (
    <div className="space-y-3">
      {members.map((member) => (
        <div key={member.id} className="flex items-center gap-3">
          <Avatar className="h-8 w-8">
            <AvatarImage src={member.user?.avatar_url} />
            <AvatarFallback>
              {member.user?.full_name?.[0] || member.user?.email[0] || "?"}
            </AvatarFallback>
          </Avatar>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">
              {member.user?.full_name || member.user?.email}
            </p>
            <p className="text-xs text-muted-foreground truncate">
              {member.user?.email}
            </p>
          </div>
          <div className="flex items-center gap-2">
            {member.member_type === "ai_agent" && (
              <Badge variant="secondary" className="text-xs">
                AI
              </Badge>
            )}
            <Badge
              variant={member.role === "owner" ? "default" : "outline"}
              className="text-xs"
            >
              {member.role}
            </Badge>
          </div>
        </div>
      ))}
    </div>
  );
}

/**
 * Team Not Found Component
 */
function TeamNotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] text-center">
      <Users className="w-12 h-12 text-muted-foreground mb-4" />
      <h3 className="text-lg font-medium mb-2">Team not found</h3>
      <p className="text-muted-foreground mb-6">
        The team you're looking for doesn't exist or you don't have access to
        it.
      </p>
      <Link to="/teams">
        <Button>Back to Teams</Button>
      </Link>
    </div>
  );
}

/**
 * Loading Skeleton
 */
function TeamDetailSkeleton() {
  return (
    <div className="container mx-auto py-6 space-y-6">
      <div className="flex items-start justify-between">
        <div className="space-y-2">
          <Skeleton className="h-8 w-64" />
          <Skeleton className="h-4 w-32" />
          <Skeleton className="h-4 w-96 mt-2" />
        </div>
        <Skeleton className="h-10 w-32" />
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        {[1, 2, 3].map((i) => (
          <Card key={i}>
            <CardHeader>
              <Skeleton className="h-4 w-20" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-8 w-16 mb-1" />
              <Skeleton className="h-3 w-32" />
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {[1, 2].map((i) => (
          <Card key={i}>
            <CardHeader>
              <Skeleton className="h-5 w-32" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-20 w-full" />
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
