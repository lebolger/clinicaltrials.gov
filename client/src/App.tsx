import {
  AppBar,
  Card,
  CardContent,
  MenuItem,
  MenuList,
  Paper,
  Stack,
  Typography,
} from "@mui/material";
import { BarChart } from "@mui/x-charts";
import { useEffect, useState } from "react";

const params = new URLSearchParams({
  pageSize: "1000",
  format: "json",
  "filter.advanced": "AREA[StartDate]RANGE[01/01/2024,MAX]",
}).toString();

type Study = {
  protocolSection: {
    conditionsModule: {
      conditions: string[];
    };
    sponsorCollaboratorsModule: {
      leadSponsor: {
        name: string;
      };
    };
  };
};

const getTopStudies = (studies: Study[]) => {
  const numStudiesBySponsor = studies.reduce<Record<string, number>>(
    (acc, study) => {
      const sponsor =
        study.protocolSection.sponsorCollaboratorsModule.leadSponsor.name;

      acc[sponsor] = (acc[sponsor] ?? 0) + 1;

      return acc;
    },
    {}
  );
  console.log({ numStudiesBySponsor });

  const topStudiesBySponsor = Object.fromEntries(
    Object.entries(numStudiesBySponsor)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
  );
  console.log({ topStudiesBySponsor });

  return topStudiesBySponsor;
};

const getTopConditions = (studies: Study[]) => {
  const numConditionsByStudy = studies.reduce<Record<string, number>>(
    (acc, study) => {
      const conditions =
        study.protocolSection.conditionsModule.conditions ?? [];

      conditions.forEach((condition) => {
        acc[condition] = (acc[condition] ?? 0) + 1;
      });

      return acc;
    },
    {}
  );
  console.log({ numConditionsByStudy });

  const topConditionsByStudy = Object.fromEntries(
    Object.entries(numConditionsByStudy)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
  );
  console.log({ topConditionsByStudy });

  return topConditionsByStudy;
};

export const App = () => {
  const [studies, setStudies] = useState<Study[]>([]);

  useEffect(() => {
    const getStudies = async () => {
      const response = await fetch(
        `https://clinicaltrials.gov/api/v2/studies?${params}`
      );
      const json = await response.json();

      setStudies(json.studies);
    };

    getStudies();
  }, []);
  console.log({ studies });

  const numStudiesBySponsor = getTopStudies(studies);
  const numConditionsByStudy = getTopConditions(studies);

  return (
    <Stack direction="column" flexGrow={1} height="100vh">
      <AppBar />

      <Stack direction="row" flexGrow={1}>
        <Paper sx={{ width: "200px" }}>
          <MenuList>
            <MenuItem>Home</MenuItem>
          </MenuList>
        </Paper>

        <Stack p={4} gap={4}>
          <Card variant="outlined">
            <CardContent>
              <Typography
                component="h2"
                variant="subtitle1"
                align="center"
                fontWeight={700}
              >
                2025 Clinical Trials: Top 10 Industry Sponsors
              </Typography>
              <BarChart
                width={1200}
                height={500}
                borderRadius={8}
                colors={["#02b2af"]}
                xAxis={[
                  {
                    scaleType: "band",
                    data: Object.keys(numStudiesBySponsor),
                  },
                ]}
                series={[
                  {
                    label: "Number of Studies",
                    data: Object.values(numStudiesBySponsor),
                    type: "bar",
                  },
                ]}
                grid={{ horizontal: true }}
                slotProps={{
                  legend: {
                    hidden: true,
                  },
                }}
              />
            </CardContent>
          </Card>

          <Card variant="outlined">
            <CardContent>
              <Typography
                component="h2"
                variant="subtitle1"
                align="center"
                fontWeight={700}
              >
                2025 Clinical Trials: Top 10 Conditions
              </Typography>
              <BarChart
                width={1200}
                height={500}
                borderRadius={8}
                colors={["#02b2af"]}
                xAxis={[
                  {
                    scaleType: "band",
                    data: Object.keys(numConditionsByStudy),
                  },
                ]}
                series={[
                  {
                    label: "Number of Conditions",
                    data: Object.values(numConditionsByStudy),
                    type: "bar",
                  },
                ]}
                grid={{ horizontal: true }}
                slotProps={{
                  legend: {
                    hidden: true,
                  },
                }}
              />
            </CardContent>
          </Card>
        </Stack>
      </Stack>
    </Stack>
  );
};
