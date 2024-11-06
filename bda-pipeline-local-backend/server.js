import { QuickSightClient, GetDashboardEmbedUrlCommand } from "@aws-sdk/client-quicksight";

const quicksightClient = new QuickSightClient({ region: process.env.AWS_REGION });

export const handler = async (event) => {
  // Parse request body
  const body = JSON.parse(event.body);
  const dashboardId = body.dashboardId;

  if (!dashboardId) {
    return {
      statusCode: 400,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify({ error: 'DashboardId is required' }),
    };
  }

  const params = {
    AwsAccountId: process.env.AWS_ACCOUNT_ID,
    DashboardId: dashboardId,
    IdentityType: 'QUICKSIGHT',
    UserArn: process.env.QUICKSIGHT_USER_ARN,
    UndoRedoDisabled: false,
    ResetDisabled: false,
    SessionLifetimeInMinutes: 60,
  };

  try {
    const command = new GetDashboardEmbedUrlCommand(params);
    const data = await quicksightClient.send(command);

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify({ embedUrl: data.EmbedUrl }),
    };
  } catch (error) {
    console.error('Error generating embed URL:', error);
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify({ error: 'Failed to retrieve embed URL' }),
    };
  }
};
