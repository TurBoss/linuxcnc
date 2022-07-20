# coding=utf-8
#
#   2022 TurBoss
#
#   This file is part of LinuxCNC.
#
#   LinuxCNC is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   LinuxCNC is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with LinuxCNC.  If not, see <http://www.gnu.org/licenses/>.

# Implementation of Andy Pugh page at https://wiki.linuxcnc.org/cgi-bin/wiki.pl?ToolDatabase
import sys

from pprint import pprint
from deepdiff import DeepDiff
from sqlalchemy.sql import exists

from .base import Session, engine, Base
from .tool_database import Spindles, Magazines, Pockets, GeomGroups, Geometries, Offsets, Tools


class ToolDBHandler:
    """Tool Database Handler
    
    """
    
    def __init__(self):
        
        Base.metadata.create_all(engine)

        self.session = Session()
        
        print("Session open.",file=sys.stderr)

    #
    # Spindles Actions
    #

    def new_spindle(self, description, active):
        
        print(f"new spindle {description}", file=sys.stderr)
        
        spindle_offsets = Offsets(
            description="spindle default values",
        )
        
        spindle = Spindles(
            description=description,
            active=active
        )
        
        spindle.offsets = [spindle_offsets]
        
        self.session.add(spindle)
        self.session.add(spindle_offsets)
        
        try:
            self.session.commit()
            print("spindle created.", file=sys.stderr)

            
        except Exception as e:
            print(e, file=sys.stderr)

        # finally:
        #     session.close()
        

    def edit_spindle(self):
        pass
    
    def delete_spindle(self):
        pass

    #
    # Magazines Actions
    #

    def new_magazine(self, description, type, num_pockets=12):
        
        print(f"new magazine, {description}", file=sys.stderr)
        
        magazines = Magazines(
            description=description,
            type=type,
            num_pockets=num_pockets
        )

        self.session.add(magazines)
        
        try:
            self.session.commit()
            print("magazine created.", file=sys.stderr)
            
        except Exception as e:
            print(e, file=sys.stderr)

        # finally:
        #     session.close()

    def edit_magazine(self):
        pass
    
    def delete_magazine(self):
        pass

    #
    # Pockets Actions
    #

    def new_pocket(self, tool_db_handler, pocket_offs=None, slot_pos=None):
               
        pocket_exist = self.session.query(exists().where(Pockets.slot_pos == slot_pos)).scalar()
        
        if pocket_exist:
            print(f"pocket in slot {slot_pos} already exist", file=sys.stderr)
            return 
        
        pocket = Pockets(
            pocket_offs=pocket_offs,
            slot_pos=slot_pos,
            magazines_id=tool_db_handler,
            tools_id=slot_pos,
            
        )
        
        self.session.add(pocket)
        
        try:
            self.session.commit()
            print(f"pocket {slot_pos} created.", file=sys.stderr)
            
        except Exception as e:
            print(e)

        # finally:
        #     session.close()
        

    def edit_pocket(self):
        pass
    
    def delete_pocket(self):
        pass

    #
    # Geometries Actions
    #

    def new_geometry(self, description, orientation=None, frontangle=None, backangle=None):
        
        geometries = Geometries(
            description=description,
            orientation=orientation,
            frontangle=frontangle,
            backangle=backangle
        )

        self.session.add(geometries)
        
        try:
            self.session.commit()
            print(f"geometry {description} created.", file=sys.stderr)
            
        except Exception as e:
            print(e, file=sys.stderr)

        # finally:
        #     session.close()
        

    def edit_geometries(self):
        pass
    
    def delete_geometries(self):
        pass

    #
    # Offsets Actions
    #

    def new_offsets(self, description, number, tool_id=None, spindle_id=None):
       
        offsets = Offsets(
            description=description,
            number=number,
            tool_id=tool_id,
            spindle_id=spindle_id
        )

        self.session.add(offsets)
        
        try:
            self.session.commit()
            print(f"Tool number {number} created", file=sys.stderr)
            
        except Exception as e:
            print(e)

        # finally:
        #     session.close()

    def edit_offsets(self):
        pass
    
    def delete_offsets(self):
        pass
    #
    # Tools Actions
    #

    def new_tool(self, description, number, magazine=1):
        
        tool_exist = self.session.query(exists().where(Tools.number == number)).scalar()
        
        if tool_exist:
            print(f"tool with munber {number} already exist", file=sys.stderr)
            return
        
        tool_offsets = Offsets(
            description="tool default values",
        )
        
        tool = Tools(
            description=description,
            number=number,
            magazines_id=magazine
        )
        
        tool.offsets = [tool_offsets]
        
        # diff = DeepDiff(tool_exist, tool, view="tree")
        #
        # pprint(diff)
        #
        # to_insert = diff.get("dictionary_item_added")
        # to_update = diff.get("values_changed")
        # to_delete = diff.get("dictionary_item_removed")
        #
        # print(to_insert)
        # print(to_update)
        # print(to_delete)
        
        self.session.add(tool)
        self.session.add(tool_offsets)
        
        try:
            self.session.commit()
            print(f"Tool number {number} created", file=sys.stderr)
            
        except Exception as e:
            print(e, file=sys.stderr)

        # finally:
        #     session.close()

    def edit_tool(self):
        pass
    
    def delete_tool(self):
        pass


def main():
    
    tool_db_handler = ToolDBHandler()
    
    tool_db_handler.new_geometry("default geometry")
    
    tool_db_handler.new_magazine("Main magazine", "linear", 12)

    for i in range(1, 12 + 1):
        tool_db_handler.new_pocket(1, None, i)

    tool_db_handler.new_spindle("Main spindle", True)
    
    for i in range(1, 30+1):
        tool_db_handler.new_tool("Tool {i}", i)

        

if __name__ == "__main__":
    main()
