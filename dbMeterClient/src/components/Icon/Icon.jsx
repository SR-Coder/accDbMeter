import { useEffect, useState } from "react";
import PropTypes from "prop-types";
import "./Icon.css";
import { AlarmOutlinedIcon } from "../../assets/Icons/Outlined/Alarm-Outlined";
import { AlarmFilledIcon } from "../../assets/Icons/Filled/Alarm-Filled";
import { ConversationOutlinedIcon } from "../../assets/Icons/Outlined/Conversation-Outlined";
import { ConversationFilledIcon } from "../../assets/Icons/Filled/Conversation-Filled";
import { GunFilledIcon } from "../../assets/Icons/Filled/Gun-Filled";
import { GunOutlinedIcon } from "../../assets/Icons/Outlined/Gun-Outlined";
import { JetFilledIcon } from "../../assets/Icons/Filled/Jet-Plane-Filled";
import { JetOutlinedIcon } from "../../assets/Icons/Outlined/Jet-Plane-Outlined";
import { MowerFilledIcon } from "../../assets/Icons/Filled/Lawnmower-Filled";
import { MowerOutlinedIcon } from "../../assets/Icons/Outlined/Lawnmower-Outlined";
import { LeavesFilledIcon } from "../../assets/Icons/Filled/Leaves-Filled";
import { LeavesOutlinedIcon } from "../../assets/Icons/Outlined/Leaves-Outlined";
import { RainFilledIcon } from "../../assets/Icons/Filled/Rain-Filled";
import { RainOutlinedIcon } from "../../assets/Icons/Outlined/Rain-Outlined";
import { SnowFilledIcon } from "../../assets/Icons/Filled/Snow-Mobile-Filled";
import { SnowOutlinedIcon } from "../../assets/Icons/Outlined/Snow-Mobile-Outlined";
import { StadiumOutlinedIcon } from "../../assets/Icons/Outlined/Stadium-Outlined";
import { StadiumFilledIcon } from "../../assets/Icons/Filled/Stadium-Filled";
import { VacuumOutlinedIcon } from "../../assets/Icons/Outlined/Vacuum-Outlined";
import { VacuumFilledIcon } from "../../assets/Icons/Filled/Vacuum-Filled";
import { AmbulanceOutlinedIcon } from "../../assets/Icons/Outlined/Ambulance-Outlined";
import { LibraryOutlinedIcon } from "../../assets/Icons/Outlined/Library-Outlined";

function Icon({ name, type }) {
  const [importedIcon, setImportedIcon] = useState(null);

  useEffect(() => {
    const getIcon = type === "outlined" ? getOutlinedIcon : getFilledIcon;
    setImportedIcon(getIcon(name));
    return () => {
      setImportedIcon(null);
    };
  }, [name, type]);

  return importedIcon || null;
}

Icon.propTypes = {
  name: PropTypes.string.isRequired,
  type: PropTypes.string,
};

const getFilledIcon = (name) => {
  console.log("name", name);
  switch (name) {
    case "alarm":
      return <AlarmFilledIcon />;
    case "conversation":
      return <ConversationFilledIcon />;
    case "gun":
      return <GunFilledIcon />;
    case "jet":
      return <JetFilledIcon />;
    case "mower":
      return <MowerFilledIcon />;
    case "leaves":
      return <LeavesFilledIcon />;
    case "rain":
      return <RainFilledIcon />;
    case "snow":
      return <SnowFilledIcon />;
    case "stadium":
      return <StadiumFilledIcon />;
    case "vacuum":
      return <VacuumFilledIcon />;

    default:
      return null;
  }
};

const getOutlinedIcon = (name) => {
  console.log("name", name);
  switch (name) {
    case "alarm":
      return <AlarmOutlinedIcon />;
    case "ambulance":
      return <AmbulanceOutlinedIcon />;
    case "conversation":
      return <ConversationOutlinedIcon />;
    case "gun":
      return <GunOutlinedIcon />;
    case "jet":
      return <JetOutlinedIcon />;
    case "mower":
      return <MowerOutlinedIcon />;
    case "leaves":
      return <LeavesOutlinedIcon />;
    case "library":
      return <LibraryOutlinedIcon />;
    case "rain":
      return <RainOutlinedIcon />;
    case "snow":
      return <SnowOutlinedIcon />;
    case "stadium":
      return <StadiumOutlinedIcon />;
    case "vacuum":
      return <VacuumOutlinedIcon />;

    default:
      return null;
  }
};

export default Icon;
